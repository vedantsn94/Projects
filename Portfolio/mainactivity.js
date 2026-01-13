// hamburger menu toggle functionality
let Hamburger = document.getElementById("hamburger");
Hamburger.addEventListener("click", () => {
  console.log("hamburger is clicked successfully");
  let Right_div = document.getElementById("menu");
  Right_div.classList.toggle("active");
});

// Contact form //
function submit() {
  let Name = document.getElementById("name").value;
  let Email = document.getElementById("email").value;
  let Message = document.getElementById("message").value;

  let templateParams = {
    name: Name, 
    email: Email,
    message: Message,
  };

  emailjs.send("service_68lp38e", "template_rolwhf4", templateParams).then(
    function (response) {
      console.log("SUCCESS!", response.status, response.text);
      alert("Message Sent Successfully!");
    },
    function (error) {
      console.log("FAILED...", error);
      alert("Failed to send message. Please try again.");
    }
  );
}

// Qualifications Popup //
let openBtn = document.getElementById("openPopup");
let popup = document.getElementById("popup");
let closeBtn = document.getElementById("closePopup");

openBtn.addEventListener("click", () => {
  popup.style.display = "flex";
});

closeBtn.addEventListener("click", () => {
  popup.style.display = "none";
});

// Certifications Popup //
let openCertBtn = document.getElementById("openCertPopup");
let certPopup = document.getElementById("certPopup");
let closeCertBtn = document.getElementById("closeCert");

openCertBtn.addEventListener("click", () => {
  certPopup.style.display = "flex";
});

closeCertBtn.addEventListener("click", () => {
  certPopup.style.display = "none";
});

