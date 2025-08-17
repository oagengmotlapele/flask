// Icon colors & classes for each contact type
const contactTypeIcons = {
  phone: { icon: "fas fa-phone", color: "#28a745", labelPrefix: "Call us at " },
  whatsapp: { icon: "fab fa-whatsapp", color: "#25D366", labelPrefix: "WhatsApp us at " },
  email: { icon: "fas fa-envelope", color: "#ea4335", labelPrefix: "Email us at " },
  facebook: { icon: "fab fa-facebook-f", color: "#1877F2", labelPrefix: "Facebook: " },
  twitter: { icon: "fab fa-twitter", color: "#1DA1F2", labelPrefix: "Twitter: " },
  instagram: { icon: "fab fa-instagram", color: "#C13584", labelPrefix: "Instagram: " },
  linkedin: { icon: "fab fa-linkedin-in", color: "#0A66C2", labelPrefix: "LinkedIn: " },
  website: { icon: "fas fa-globe", color: "#0073e6", labelPrefix: "Visit our website: " },
  location: { icon: "fas fa-map-marker-alt", color: "#d93025", labelPrefix: "Find us at: " },
  postal: { icon: "fas fa-envelope-open", color: "#6c757d", labelPrefix: "Postal address: " }
};

const contactCardsDiv = document.getElementById('contactCards');
const addContactBtn = document.getElementById('addContactBtn');
const modalOverlay = document.getElementById('modalOverlay');
const closeModalBtn = document.getElementById('closeModalBtn');
const cancelBtn = document.getElementById('cancelBtn');
const contactForm = document.getElementById('contactForm');
const contactTypeSelect = document.getElementById('contactType');
const contactValueInput = document.getElementById('contactValue');
const contactUrlInput = document.getElementById('contactUrl');
const contactUrlLabel = document.getElementById('contactUrlLabel');
const contactValueLabel = document.getElementById('contactValueLabel');

// Render cards from initialContacts (from Flask)
function renderCards(contacts) {
  contactCardsDiv.innerHTML = '';

  contacts.forEach(contact => {
    const typeInfo = contactTypeIcons[contact.contact_type] || {
      icon: "fas fa-info-circle",
      color: "#888",
      labelPrefix: ""
    };

    // For clickable types with URLs, show clickable link else text + copy number on click
    const isClickableLink = ['facebook','twitter','instagram','linkedin','website'].includes(contact.contact_type);
    const isPhoneLike = ['phone','whatsapp','email'].includes(contact.contact_type);

    const card = document.createElement('div');
    card.className = 'contact-card';

    const icon = document.createElement('i');
    icon.className = typeInfo.icon + ' contact-icon';
    icon.style.color = typeInfo.color;

    const text = document.createElement('span');
    text.className = 'contact-text';

    // Compose the label text
    const labelText = typeInfo.labelPrefix + contact.contact_value;

    if (isClickableLink) {
      const link = document.createElement('a');
      link.href = contact.contact_value;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.style.color = "inherit";
      link.style.textDecoration = "none";
      link.textContent = labelText;

      // Hover effect on link
      link.addEventListener('mouseenter', () => {
        link.style.color = '#0073e6';
      });
      link.addEventListener('mouseleave', () => {
        link.style.color = 'inherit';
      });

      text.appendChild(link);
    } else if (isPhoneLike) {
      text.textContent = labelText;
      card.addEventListener('click', () => {
        copyToClipboard(contact.contact_value);
        showToast('Copied to clipboard: ' + contact.contact_value);
      });
    } else {
      // fallback text
      text.textContent = labelText;
    }

    card.appendChild(icon);
    card.appendChild(text);
    contactCardsDiv.appendChild(card);
  });
}

// Copy text to clipboard
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).catch(() => {
    // fallback for older browsers
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    textarea.remove();
  });
}

// Toast popup for copy notification
function showToast(message) {
  const toast = document.createElement('div');
  toast.textContent = message;
  toast.style.position = 'fixed';
  toast.style.bottom = '20px';
  toast.style.left = '50%';
  toast.style.transform = 'translateX(-50%)';
  toast.style.backgroundColor = '#333';
  toast.style.color = '#fff';
  toast.style.padding = '10px 20px';
  toast.style.borderRadius = '5px';
  toast.style.opacity = '1';
  toast.style.transition = 'opacity 0.5s ease-out';
  toast.style.zIndex = '10000';

  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 500);
  }, 1500);
}

// Show/hide modal
addContactBtn.addEventListener('click', () => {
  modalOverlay.style.display = 'flex';
  contactForm.reset();
  contactUrlInput.style.display = 'none';
  contactUrlLabel.style.display = 'none';
  contactValueInput.required = true;
  contactUrlInput.required = false;
});

closeModalBtn.addEventListener('click', () => {
  modalOverlay.style.display = 'none';
});

cancelBtn.addEventListener('click', () => {
  modalOverlay.style.display = 'none';
});

// Adjust form inputs based on contact type
contactTypeSelect.addEventListener('change', () => {
  const val = contactTypeSelect.value;
  const needsUrl = ['facebook','twitter','instagram','linkedin','website'].includes(val);
  const needsValue = !needsUrl;

  if (needsUrl) {
    contactUrlInput.style.display = 'block';
    contactUrlLabel.style.display = 'block';
    contactUrlInput.required = true;

    contactValueInput.style.display = 'none';
    contactValueLabel.style.display = 'none';
    contactValueInput.required = false;
  } else {
    contactUrlInput.style.display = 'none';
    contactUrlLabel.style.display = 'none';
    contactUrlInput.required = false;

    contactValueInput.style.display = 'block';
    contactValueLabel.style.display = 'block';
    contactValueInput.required = true;
  }
});

// On page load render cards
document.addEventListener('DOMContentLoaded', () => {
  renderCards(initialContacts);
});
