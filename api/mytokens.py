from rest_framework_simplejwt.tokens import *


class MyToken(Token):
    """
    A class which validates and wraps an existing JWT or can be used to build a
    new JWT.
    """

    token_type: Optional[str] = None
    lifetime: Optional[timedelta] = None

    def __init__(self, token: Optional["Token"] = None, verify: bool = True) -> None:
        """
        !!!! IMPORTANT !!!! MUST raise a TokenError with a user-facing error
        message if the given token is invalid, expired, or otherwise not safe
        to use.
        """
        if self.token_type is None or self.lifetime is None:
            raise TokenError(_("Cannot create token with no type or lifetime"))

        self.token = token
        self.current_time = aware_utcnow()

        print("token.py: Token: __init__: token: ", token)

        # Set up token
        if token is not None:
            # An encoded token was provided
            token_backend = self.get_token_backend()

            # Decode token
            try:
                self.payload = token_backend.decode(token, verify=verify)
            except TokenBackendError:
                raise TokenError(_("Token is invalid or expired"))

            if verify:
                self.verify()
        else:
            # New token.  Skip all the verification steps.
            self.payload = {api_settings.TOKEN_TYPE_CLAIM: self.token_type}

            # Set "exp" and "iat" claims with default value
            self.set_exp(from_time=self.current_time, lifetime=self.lifetime)
            self.set_iat(at_time=self.current_time)
            print("token.py: Token: __init__: self.payload: ", self.payload)

            # Set "jti" claim
            self.set_jti()

    def verify(self) -> None:
        """
        Performs additional validation steps which were not performed when this
        token was decoded.  This method is part of the "public" API to indicate
        the intention that it may be overridden in subclasses.
        """
        # According to RFC 7519, the "exp" claim is OPTIONAL
        # (https://tools.ietf.org/html/rfc7519#section-4.1.4).  As a more
        # correct behavior for authorization tokens, we require an "exp"
        # claim.  We don't want any zombie tokens walking around.
        self.check_exp()

        # If the defaults are not None then we should enforce the
        # requirement of these settings.As above, the spec labels
        # these as optional.
        if (
            api_settings.JTI_CLAIM is not None
            and api_settings.JTI_CLAIM not in self.payload
        ):
            raise TokenError(_("Token has no id"))

        if api_settings.TOKEN_TYPE_CLAIM is not None:
            self.verify_token_type()

    def verify_token_type(self) -> None:
        """
        Ensures that the token type claim is present and has the correct value.
        """
        try:
            token_type = self.payload[api_settings.TOKEN_TYPE_CLAIM]
        except KeyError:
            raise TokenError(_("Token has no type"))

        if self.token_type != token_type:
            raise TokenError(_("Token has wrong type"))

    @classmethod
    def for_user(cls, user: AuthUser) -> "Token":
        """
        Returns an authorization token for the given user that will be provided
        after authenticating the user's credentials.
        """
        user_id = getattr(user, api_settings.USER_ID_FIELD)
        if not isinstance(user_id, int):
            user_id = str(user_id)

        token = cls()
        token[api_settings.USER_ID_CLAIM] = user_id
        print("token for ")

        if api_settings.CHECK_REVOKE_TOKEN:
            token[api_settings.REVOKE_TOKEN_CLAIM] = get_md5_hash_password(
                user.password
            )

        return token

    _token_backend: Optional["TokenBackend"] = None

    @property
    def token_backend(self) -> "TokenBackend":
        if self._token_backend is None:
            self._token_backend = import_string(
                "rest_framework_simplejwt.state.token_backend"
            )
        return self._token_backend

    def get_token_backend(self) -> "TokenBackend":
        # Backward compatibility.
        return self.token_backend


class MyAccessToken(MyToken):
    token_type = "access"
    lifetime = api_settings.ACCESS_TOKEN_LIFETIME


class MyRefreshToken(BlacklistMixin, MyToken):
    token_type = "refr"
    lifetime = api_settings.REFRESH_TOKEN_LIFETIME
    no_copy_claims = (
        api_settings.TOKEN_TYPE_CLAIM,
        "exp",
        # Both of these claims are included even though they may be the same.
        # It seems possible that a third party token might have a custom or
        # namespaced JTI claim as well as a default "jti" claim.  In that case,
        # we wouldn't want to copy either one.
        api_settings.JTI_CLAIM,
        "jti",
    )
    access_token_class = AccessToken

    @property
    def access_token(self) -> AccessToken:
        """
        Returns an access token created from this refresh token.  Copies all
        claims present in this refresh token to the new access token except
        those claims listed in the `no_copy_claims` attribute.
        """
        print("token.py: MyRefreshToken: access_token: self.payload: ", self.payload)
        access = self.access_token_class()

        # Use instantiation time of refresh token as relative timestamp for
        # access token "exp" claim.  This ensures that both a refresh and
        # access token expire relative to the same time if they are created as
        # a pair.
        access.set_exp(from_time=self.current_time)

        no_copy = self.no_copy_claims
        for claim, value in self.payload.items():
            if claim in no_copy:
                continue
            access[claim] = value

        access['username'] = user.username
        access['email'] = user.email
        access['first_name'] = user.first_name
        access['last_name'] = user.last_name
        # Safely access image URL
        access['image'] = user.image.url if user.image else None
        access['gender'] = user.gender
        access['phone'] = user.phone
        access['role'] = user.role

        print(access)
        print(self.payload)

        return access
