document.getElementById('settings-icon').addEventListener('click', function() {
    event.preventDefault();
          document.getElementById('themeModal').style.display = 'block';
      });

      document.getElementsByClassName('close')[0].addEventListener('click', function() {
          document.getElementById('themeModal').style.display = 'none';
      });

      document.getElementById('theme-select').addEventListener('change', function() {
          var theme = this.value;
          document.getElementById('theme-link').href = theme;
          localStorage.setItem('selectedTheme', theme);
      });

$(document).ready(function() {
    var theme=localStorage.getItem('selectedTheme');
    if(theme){
    document.getElementById('theme-link').href =theme;
    document.getElementById('theme-select').value=theme;
    }
    else{
      document.getElementById('theme-link').href ="{{ url_for('static', filename='css/winterfrost.css') }}";
    }
});
window.addEventListener('load', function () {
    document.body.classList.add('loaded');
});
