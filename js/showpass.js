const items = document.querySelectorAll(".headline button");

function toggleheadline() {
  const itemToggle = this.getAttribute('aria-expanded');
  for (i = 0; i < items.length; i++) {
    items[i].setAttribute('aria-expanded', 'false');
  }
  if (itemToggle == 'false') {
    this.setAttribute('aria-expanded', 'true');
  }
}

items.forEach(item => item.addEventListener('click', toggleheadline));

function showpas() {
  var icon = document.getElementById("eyeicon")
  var x = document.getElementById("password");
  if (x.type === "password") {
    x.type = "text";
    icon.classList.remove("fa-eye");
    icon.classList.add("fa-eye-slash");
  } else {
    icon.classList.add("fa-eye");
    icon.classList.remove("fa-eye-slash");
    x.type = "password";
  }
}

function showpas2() {
  var icon = document.getElementById("eyeicon2")
  var x = document.getElementById("password2");
  if (x.type === "password") {
    x.type = "text";
    icon.classList.remove("fa-eye");
    icon.classList.add("fa-eye-slash");
  } else {
    icon.classList.add("fa-eye");
    icon.classList.remove("fa-eye-slash");
    x.type = "password";
  }
}

function showpas3() {
  var icon = document.getElementById("eyeicon3")
  var x = document.getElementById("password3");
  if (x.type === "password") {
    x.type = "text";
    icon.classList.remove("fa-eye");
    icon.classList.add("fa-eye-slash");
  } else {
    icon.classList.add("fa-eye");
    icon.classList.remove("fa-eye-slash");
    x.type = "password";
  }
}