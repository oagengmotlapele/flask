document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('team1-cardModal');
  const addBtn = document.getElementById('team1-addCardBtn');
  const cancelBtn = document.getElementById('team1-cancelBtn');
  const form = document.getElementById('team1-cardForm');
  const posSelect = document.getElementById('team1-positionSelect');
  const cardList = document.getElementById('team1-cardList');

  let contacts = [];
  let editIndex = null;

  // Populate position select (1 to 10)
  function fillPositions() {
    posSelect.innerHTML = '';
    for (let i = 1; i <= 10; i++) {
      const opt = document.createElement('option');
      opt.value = i;
      opt.textContent = `Position at ${i}`;
      posSelect.appendChild(opt);
    }
  }
  fillPositions();

  // Open modal for adding
  addBtn.addEventListener('click', () => {
    editIndex = null;
    form.reset();
    modal.classList.add('active');
  });

  // Close modal
  cancelBtn.addEventListener('click', () => {
    modal.classList.remove('active');
  });

  // Render cards function
  function renderCards() {
    cardList.innerHTML = '';
    contacts.forEach((contact, i) => {
      const card = document.createElement('div');
      card.className = 'team1-card';
      card.dataset.index = i;

      const img = document.createElement('img');
      img.src = contact.image || '/static/default-user.png'; // You need a local fallback image
      img.alt = contact.fullName;
      img.style.width = '80px';
      img.style.height = '80px';
      img.style.borderRadius = '50%';
      card.appendChild(img);

      const content = document.createElement('div');
      content.className = 'team1-card-content';
      content.innerHTML = `
        <h3>${escapeHtml(contact.fullName)}</h3>
        <h4>${escapeHtml(contact.role)}</h4>
        <p>${escapeHtml(contact.description)}</p>
        <div class="team1-card-footer">
          <a href="${escapeHtml(contact.facebook)}" target="_blank" rel="noopener">Facebook</a>
          <a href="${escapeHtml(contact.linkedin)}" target="_blank" rel="noopener">LinkedIn</a>
          <a href="${escapeHtml(contact.twitter)}" target="_blank" rel="noopener">Twitter</a>
          <a href="${escapeHtml(contact.whatsapp)}" target="_blank" rel="noopener">WhatsApp</a>
        </div>
      `;
      card.appendChild(content);

      // Edit button
      const editBtn = document.createElement('button');
      editBtn.textContent = '✏️';
      editBtn.type = 'button';
      editBtn.addEventListener('click', () => openEdit(i));
      card.appendChild(editBtn);

      // Delete button
      const delBtn = document.createElement('button');
      delBtn.textContent = '🗑';
      delBtn.type = 'button';
      delBtn.addEventListener('click', () => deleteContact(i));
      card.appendChild(delBtn);

      cardList.appendChild(card);
    });
  }

  // Escape HTML helper
  function escapeHtml(text) {
    return text.replace(/[&<>"']/g, function(m) {
      return {'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[m];
    });
  }

  // Open modal with contact data for editing
  function openEdit(i) {
    editIndex = i;
    const c = contacts[i];
    form.fullName.value = c.fullName;
    form.role.value = c.role;
    form.description.value = c.description;
    form.facebook.value = c.facebook;
    form.linkedin.value = c.linkedin;
    form.twitter.value = c.twitter;
    form.whatsapp.value = c.whatsapp;
    posSelect.value = i + 1;
    modal.classList.add('active');
  }

  // Delete contact
  function deleteContact(i) {
    if (confirm('Delete this contact?')) {
      contacts.splice(i, 1);
      renderCards();
    }
  }

  // Handle form submit (for demo, just local)
  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const data = {
      fullName: form.fullName.value.trim(),
      role: form.role.value.trim(),
      description: form.description.value.trim(),
      facebook: form.facebook.value.trim(),
      linkedin: form.linkedin.value.trim(),
      twitter: form.twitter.value.trim(),
      whatsapp: form.whatsapp.value.trim(),
      image: null
    };

    const file = form.imageUpload.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        data.image = reader.result;
        saveContact(data);
      };
      reader.readAsDataURL(file);
    } else {
      saveContact(data);
    }
  });

  // Save contact locally
  function saveContact(data) {
    if (editIndex !== null) {
      contacts.splice(editIndex, 1);
    }
    const pos = parseInt(posSelect.value, 10) - 1;
    contacts.splice(pos, 0, data);
    modal.classList.remove('active');
    renderCards();
  }

  renderCards();
});
