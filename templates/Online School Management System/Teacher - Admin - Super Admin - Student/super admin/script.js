function showSection(sectionId) {
  const sections = document.querySelectorAll('.section');
  sections.forEach(section => {
      section.classList.remove('active');
      section.style.display = 'none';
  });
  const activeSection = document.getElementById(sectionId);
  activeSection.classList.add('active');
  activeSection.style.display = 'block';

  const navLinks = document.querySelectorAll('.sidebar a');
  navLinks.forEach(link => link.classList.remove('active'));
  document.querySelector(`.sidebar a[href="#${sectionId}"]`).classList.add('active');
}

function generateKeys() {
  // ... (keep existing code)
}

function exportKeys() {
  // ... (keep existing code)
}

let chart;

function generateReport() {
  const totalSchools = Math.floor(Math.random() * 100);
  const totalAdmins = Math.floor(Math.random() * 500);
  const totalStudents = Math.floor(Math.random() * 10000);
  const activeKeys = Math.floor(Math.random() * 1000);

  document.getElementById('total-schools').textContent = totalSchools;
  document.getElementById('total-admins').textContent = totalAdmins;
  document.getElementById('total-students').textContent = totalStudents;
  document.getElementById('active-keys').textContent = activeKeys;

  if (chart) {
      chart.destroy();
  }

  const ctx = document.getElementById('analytics-chart').getContext('2d');
  chart = new Chart(ctx, {
      type: 'bar',
      data: {
          labels: ['Schools', 'Admins', 'Students', 'Active Keys'],
          datasets: [{
              label: 'System Statistics',
              data: [totalSchools, totalAdmins, totalStudents, activeKeys],
              backgroundColor: [
                  'rgba(255, 99, 132, 0.8)',
                  'rgba(54, 162, 235, 0.8)',
                  'rgba(255, 206, 86, 0.8)',
                  'rgba(75, 192, 192, 0.8)'
              ],
              borderColor: [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)'
              ],
              borderWidth: 1
          }]
      },
      options: {
          responsive: true,
          scales: {
              y: {
                  beginAtZero: true
              }
          },
          animation: {
              duration: 1500,
              easing: 'easeInOutQuart'
          }
      }
  });

  alert('Report generated successfully!');
}

function runSecurityAudit() {
  // ... (keep existing code)
}

document.addEventListener('DOMContentLoaded', () => {
  showSection('profile');
  generateReport(); // Generate initial report
});