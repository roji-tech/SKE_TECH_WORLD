 // Close the overlay when the user clicks on the close button (x)
 var closeOverlay = document.querySelectorAll('.close');
 closeOverlay.forEach(function(button) {
     button.addEventListener('click', function() {
         var overlay = button.closest('.overlay');
         overlay.classList.remove('show');
     });
 });

 // Close the overlay when the user clicks outside of it
 window.addEventListener('click', function(event) {
     var overlays = document.querySelectorAll('.overlay');
     overlays.forEach(function(overlay) {
         if (event.target === overlay) {
             overlay.classList.remove('show');
         }
     });
 });

 // Overlay for Add button
 document.getElementById('add').addEventListener('click', function(event) {
     event.preventDefault();
     var subjectContainer = document.getElementById('subjectContainer');
     var newSubjectField = document.createElement('div');
     newSubjectField.classList.add('inline-f');
     newSubjectField.innerHTML = '<label for="Subject" class="class">Subject</label><input type="text" name="Subject" class="input">';
     subjectContainer.appendChild(newSubjectField);
 });

 // Overlay for Save button
 document.getElementById('save').addEventListener('click', function(event) {
     event.preventDefault();
     document.getElementById('saveOverlay').classList.add('show');
 });

 // Overlay for Cancel button
 document.getElementById('cancel').addEventListener('click', function(event) {
     event.preventDefault();
     document.getElementById('cancelOverlay').classList.add('show');
 });

 // Logic for add overlay
 document.getElementById('confirmAdd').addEventListener('click', function() {
     document.getElementById('addOverlay').classList.remove('show');
     document.getElementById('successOverlay').classList.add('show');
 });

 document.getElementById('closeAddOverlay').addEventListener('click', function() {
     document.getElementById('addOverlay').classList.remove('show');
 });

 // Logic for save overlay
 document.getElementById('confirmSave').addEventListener('click', function() {
     document.getElementById('saveOverlay').classList.remove('show');
     document.getElementById('successOverlay').classList.add('show');
 });

 document.getElementById('closeSaveOverlay').addEventListener('click', function() {
     document.getElementById('saveOverlay').classList.remove('show');
 });

 // Logic for cancel overlay
 document.getElementById('confirmCancel').addEventListener('click', function() {
     document.getElementById('cancelOverlay').classList.remove('show');
 });

 document.getElementById('closeCancelOverlay').addEventListener('click', function() {
     document.getElementById('cancelOverlay').classList.remove('show');
 });

 // Close the success overlay
 document.getElementById('closeSuccessOverlay').addEventListener('click', function() {
     document.getElementById('successOverlay').classList.remove('show');
 });