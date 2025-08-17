
    (() => {
      const contacts = [
        {
          contactType: "phone",
          contactValue: "+267 72693981",
        },
        {
          contactType: "whatsapp",
          contactValue: "+267 72693981",
        },
        {
          contactType: "email",
          contactValue: "oagengmtlapele@gmail.com",
        },
        {
          contactType: "facebook",
          contactValue: "https://facebook.com/65bugs",
        },
        {
          contactType: "location",
          contactValue: "Molepolole, Botswana",
        },
      ];

      const contactCards = document.getElementById("contactCards");
      const addContactBtn = document.getElementById("addContactBtn");
      const modalOverlay = document.getElementById("modalOverlay");
      const closeModalBtn = document.getElementById("closeModalBtn");
      const contactForm = document.getElementById("contactForm");
      const contactTypeSelect = document.getElementById("contactType");
      const contactValueInput = document.getElementById("contactValue");
      const contactUrlInput = document.getElementById("contactUrl");
      const valueLabel = document.getElementById("valueLabel");
      const cancelBtn = document.getElementById("cancelBtn");
      const toast = document.getElementById("toast");

      let editingIndex = -1;

      const iconMap = {
        phone: "fas fa-phone",
        whatsapp: "fab fa-whatsapp",
        email: "fas fa-envelope",
        facebook: "fab fa-facebook-f",
        twitter: "fab fa-twitter",
        instagram: "fab fa-instagram",
        linkedin: "fab fa-linkedin-in",
        website: "fas fa-globe",
        location: "fas fa-map-marker-alt",
        postal: "fas fa-mail-bulk",
      };

      const ctaTextMap = {
        phone: (val) => `Call us at ${val}`,
        whatsapp: (val) => `WhatsApp us at ${val}`,
        email: (val) => `Email us at ${val}`,
        facebook: (_) => "Visit our Facebook page",
        twitter: (_) => "Visit our Twitter profile",
        instagram: (_) => "Visit our Instagram",
        linkedin: (_) => "Visit our LinkedIn",
        website: (_) => "Visit our Website",
        location: (_) => "Click to find where we are located",
        postal: (val) => `Postal address: ${val}`,
      };

      const urlRequiredTypes = [
        "facebook",
        "twitter",
        "instagram",
        "linkedin",
        "website",
      ];

      const validators = {
        phone: (val) => /^\+?\d[\d\s-]{5,}$/.test(val),
        whatsapp: (val) => /^\+?\d[\d\s-]{5,}$/.test(val),
        email: (val) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val),
        facebook: (val) => /^https?:\/\/(www\.)?facebook\.com\/.+$/i.test(val),
        twitter: (val) => /^https?:\/\/(www\.)?twitter\.com\/.+$/i.test(val),
        instagram: (val) => /^https?:\/\/(www\.)?instagram\.com\/.+$/i.test(val),
        linkedin: (val) => /^https?:\/\/(www\.)?linkedin\.com\/.+$/i.test(val),
        website: (val) => /^https?:\/\/.+$/i.test(val),
        location: (val) => val.trim().length > 0,
        postal: (val) => val.trim().length > 0,
      };

      function updateInputFields() {
        const type = contactTypeSelect.value;
        if (!type) {
          contactValueInput.style.display = "block";
          contactUrlInput.style.display = "none";
          contactValueInput.required = true;
          contactUrlInput.required = false;
          valueLabel.textContent = "Contact Details";
          contactValueInput.placeholder = "Enter details";
          contactValueInput.type = "text";
          return;
        }

        if (urlRequiredTypes.includes(type)) {
          contactUrlInput.style.display = "block";
          contactValueInput.style.display = "none";
          contactUrlInput.required = true;
          contactValueInput.required = false;
          valueLabel.textContent = "URL";
          contactUrlInput.placeholder = `Enter ${type} URL`;
          contactUrlInput.type = "url";
        } else {
          contactValueInput.style.display = "block";
          contactUrlInput.style.display = "none";
          contactValueInput.required = true;
          contactUrlInput.required = false;
          valueLabel.textContent = "Contact Details";
          contactValueInput.placeholder = "Enter details";

          if (type === "email") {
            contactValueInput.type = "email";
          } else {
            contactValueInput.type = "text";
          }
        }
      }

      function showToast(message) {
        toast.textContent = message;
        toast.classList.add("show");
        setTimeout(() => {
          toast.classList.remove("show");
        }, 1500);
      }

      function render() {
        contactCards.innerHTML = "";

        // Find first phone/whatsapp/email index
        const firstNumberIndex = contacts.findIndex((c) =>
          ["phone", "whatsapp", "email"].includes(c.contactType)
        );

        contacts.forEach((contact, i) => {
          const iconClass = iconMap[contact.contactType] || "fas fa-question-circle";
          const ctaText = ctaTextMap[contact.contactType]
            ? ctaTextMap[contact.contactType](contact.contactValue)
            : contact.contactValue;

          let href = null;
          if (urlRequiredTypes.includes(contact.contactType)) {
            href = contact.contactValue;
          } else if (contact.contactType === "phone" || contact.contactType === "whatsapp") {
            href =
              contact.contactType === "whatsapp"
                ? `https://wa.me/${contact.contactValue.replace(/[^\d]/g, "")}`
                : `tel:${contact.contactValue.replace(/\s+/g, "")}`;
          } else if (contact.contactType === "email") {
            href = `mailto:${contact.contactValue}`;
          } else if (contact.contactType === "location") {
            href = `https://www.google.com/maps/search/${encodeURIComponent(
              contact.contactValue
            )}`;
          } else if (contact.contactType === "postal") {
            href = `https://www.google.com/search?q=${encodeURIComponent(contact.contactValue)}`;
          }

          let dataPhoneCard = "false";
          if (["phone", "whatsapp", "email"].includes(contact.contactType)) {
            dataPhoneCard = i === firstNumberIndex ? "true" : "false";
          } else {
            dataPhoneCard = "true";
          }

          const card = document.createElement("div");
          card.className = "contact-card";
          card.dataset.index = i;
          card.dataset.phoneCard = dataPhoneCard;

          let innerHTML;
          if (href) {
            innerHTML = `
              <a href="${href}" target="_blank" rel="noopener noreferrer" class="contact-info" title="${ctaText}">
                <i class="${iconClass}" aria-hidden="true"></i>
                <span class="contact-text">${ctaText}</span>
              </a>
            `;
          } else {
            innerHTML = `
              <div class="contact-info" title="Click to copy">
                <i class="${iconClass}" aria-hidden="true"></i>
                <span class="contact-text">${ctaText}</span>
              </div>
            `;
          }

          innerHTML += `
            <div class="actions">
              <button class="edit-btn" aria-label="Edit contact method">✏️</button>
              <button class="delete" aria-label="Delete contact method">🗑️</button>
            </div>
          `;

          card.innerHTML = innerHTML;
          contactCards.appendChild(card);
        });
      }

      function openModal(index = -1) {
        editingIndex = index;
        if (index >= 0) {
          const contact = contacts[index];
          contactTypeSelect.value = contact.contactType;
          updateInputFields();
          if (urlRequiredTypes.includes(contact.contactType)) {
            contactUrlInput.value = contact.contactValue;
            contactValueInput.value = "";
          } else {
            contactValueInput.value = contact.contactValue;
            contactUrlInput.value = "";
          }
        } else {
          contactForm.reset();
          contactUrlInput.style.display = "none";
          contactValueInput.style.display = "block";
          contactValueInput.required = true;
          contactUrlInput.required = false;
          editingIndex = -1;
        }
        modalOverlay.classList.add("active");
        contactTypeSelect.focus();
      }

      function closeModal() {
        modalOverlay.classList.remove("active");
      }

      addContactBtn.addEventListener("click", () => openModal());

      closeModalBtn.addEventListener("click", closeModal);
      cancelBtn.addEventListener("click", (e) => {
        e.preventDefault();
        closeModal();
      });

      contactTypeSelect.addEventListener("change", updateInputFields);

      contactForm.addEventListener("submit", (e) => {
        e.preventDefault();

        const type = contactTypeSelect.value;
        let val = "";
        if (urlRequiredTypes.includes(type)) {
          val = contactUrlInput.value.trim();
        } else {
          val = contactValueInput.value.trim();
        }

        // Validate presence
        if (!type || !val) {
          alert("Please fill in required fields.");
          return;
        }

        // Validate format
        if (!validators[type](val)) {
          alert("Please enter a valid " + type + "!");
          return;
        }

        const newContact = { contactType: type, contactValue: val };

        if (editingIndex >= 0) {
          contacts[editingIndex] = newContact;
        } else {
          contacts.push(newContact);
        }

        closeModal();
        render();
      });

      contactCards.addEventListener("click", (e) => {
        const card = e.target.closest(".contact-card");
        if (!card) return;

        const index = Number(card.dataset.index);

        // Delete button
        if (e.target.classList.contains("delete")) {
          if (confirm("Are you sure you want to delete this contact method?")) {
            contacts.splice(index, 1);
            render();
          }
          return;
        }

        // Edit button
        if (e.target.classList.contains("edit-btn")) {
          openModal(index);
          return;
        }

        // Copy on click if no href (non-link)
        const infoDiv = e.target.closest(".contact-info");
        if (infoDiv && !infoDiv.href) {
          const text = infoDiv.querySelector(".contact-text").textContent;
          navigator.clipboard.writeText(text).then(() => {
            showToast("Copied: " + text);
          });
        }
      });


    })();
