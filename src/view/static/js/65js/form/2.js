// ======== AUTO-GENERATED VALIDATION SCRIPT ========

// Utility: toggle valid/invalid icon for each criteria point
function setCriteriaPointIcon(id, valid) {
    const iconContainer = document.getElementById(id + "-icon");
    if (!iconContainer) return;

    const icon = iconContainer.querySelector("i");
    if (!icon) return;

    icon.classList.remove("fa-check", "fa-times");
    iconContainer.classList.remove("valid", "invalid");

    if (valid) {
        icon.classList.add("fas", "fa-check");
        iconContainer.classList.add("valid");
    } else {
        icon.classList.add("fas", "fa-times");
        iconContainer.classList.add("invalid");
    }
}

// Utility: update broken line color
function updateBrokenLineColor(id, valid) {
    const el = document.getElementById("broken-" + id);
    if (!el) return;
    el.classList.remove("valid", "invalid");
    el.classList.add(valid ? "valid" : "invalid");
}

// Utility: update the main field error icon
function updateErrorIcon(id, valid) {
    const icon = document.getElementById(id + "-error-icon");
    if (!icon) return;
    icon.classList.remove("fa-check-circle", "fa-times-circle");
    icon.classList.remove("valid", "invalid");
    
    if (valid) {
        icon.classList.add("fas", "fa-check-circle");
        icon.classList.add("valid");
    } else {
        icon.classList.add("fas", "fa-times-circle");
        icon.classList.add("invalid");
    }
}

// Utility: show criteria panel on focus
function attachFocusHandler(id) {
    const input = document.getElementById(id + "-input");
    const panel = document.getElementById(id + "-criteria-panel");
    if (input && panel) {
        input.addEventListener("focus", () => {
            panel.style.display = "block";
        });
        input.addEventListener("blur", () => {
            panel.style.display = "none";
        });
    }
}

// Utility: test regex
function testRegex(pattern, value) {
    const re = new RegExp(pattern);
    return re.test(value);
}

// Utility: get input value
function getValue(id) {
    const el = document.getElementById(id + "-input");
    return el ? el.value : "";
}

// === Username ===
try{
attachFocusHandler("username");
document.getElementById("username-input").addEventListener("input", function() {
    
    const value = getValue("username");
    let allValid = true;

    let valid_length = testRegex("^.{3,15}$", value);
    setCriteriaPointIcon("username-length", valid_length);
    if (!valid_length) allValid = false;

    let valid_validchars = testRegex("^[a-zA-Z0-9]+$", value);
    setCriteriaPointIcon("username-validchars", valid_validchars);
    if (!valid_validchars) allValid = false;

    updateBrokenLineColor("username", allValid);
    updateErrorIcon("username", allValid);
});
} catch (e) {
    console.error("Error attaching event listener:", e);
}

// === First Name ===
try{
attachFocusHandler("first-name");
document.getElementById("first-name-input").addEventListener("input", function() {
    
    const value = getValue("first-name");
    let allValid = true;

    let valid_length = testRegex("^.{3,15}$", value);
    setCriteriaPointIcon("first-name-length", valid_length);
    if (!valid_length) allValid = false;

    let valid_validchars = testRegex("^[a-zA-Z0-9]+$", value);
    setCriteriaPointIcon("first-name-validchars", valid_validchars);
    if (!valid_validchars) allValid = false;

    updateBrokenLineColor("first-name", allValid);
    updateErrorIcon("first-name", allValid);
});
} catch (e) {
    console.error("Error attaching event listener:", e);
}

// === Password ===
try{
attachFocusHandler("password");
document.getElementById("password-input").addEventListener("input", function() {
    
    const value = getValue("password");
    let allValid = true;

    let valid_length = testRegex("^.{8,}$", value);
    setCriteriaPointIcon("password-length", valid_length);
    if (!valid_length) allValid = false;

    let valid_uppercase = testRegex(".*[A-Z].*", value);
    setCriteriaPointIcon("password-uppercase", valid_uppercase);
    if (!valid_uppercase) allValid = false;

    let valid_lowercase = testRegex(".*[a-z].*", value);
    setCriteriaPointIcon("password-lowercase", valid_lowercase);
    if (!valid_lowercase) allValid = false;

    let valid_special = testRegex(".*[!@#$%^&*].*", value);
    setCriteriaPointIcon("password-special", valid_special);
    if (!valid_special) allValid = false;

    let valid_number = testRegex(".*[0-9].*", value);
    setCriteriaPointIcon("password-number", valid_number);
    if (!valid_number) allValid = false;

    updateBrokenLineColor("password", allValid);
    updateErrorIcon("password", allValid);
});
} catch (e) {
    console.error("Error attaching event listener:", e);
}

// === Confirm Password ===
try{
attachFocusHandler("confirm-password");
document.getElementById("confirm-password-input").addEventListener("input", function() {
    
    const value = getValue("confirm-password");
    let allValid = true;

    let match = value === getValue("password");
    setCriteriaPointIcon("confirm-password-match", match);
    if (!match) allValid = false;

    updateBrokenLineColor("confirm-password", allValid);
    updateErrorIcon("confirm-password", allValid);
});
} catch (e) {
    console.error("Error attaching event listener:", e);
}

// === Gender ===
const radios_gender = document.getElementsByName("gender");
radios_gender.forEach(r => r.addEventListener("change", () => {
    let selected = Array.from(radios_gender).some(r => r.checked);
    setCriteriaPointIcon("gender-selected", selected);
    updateBrokenLineColor("gender", selected);
    updateErrorIcon("gender", selected);
}));

try{
attachFocusHandler("interest");
function interest() {
   let varValid = false;
   // Select all checkboxes with class 'interest-input' AND type checkbox
   const checkboxes = document.querySelectorAll('input[name="interest"]');
   checkboxes.forEach(chk => {
      chk.addEventListener('change', function() {
      // Check if at least one checkbox is checked
      varValid = Array.from(checkboxes).some(box => box.checked);
      setCriteriaPointIcon('interest', varValid);
      updateBrokenLineColor('interest', varValid);
      updateErrorIcon('interest', varValid);
      console.log('varValid:', varValid, 'Any checked:', varValid);
      });
   });
}
interest();
} catch (e) {
    console.error("Error attaching event listener:", e);
}

// === Favorite Color ===
try{
document.addEventListener('DOMContentLoaded', function() {
  console.log("cOLOR DOM  loaded");
  attachFocusHandler("favorite-color");
  const colorInput = document.getElementById('favorite-color-input');
    if (colorInput) {
        colorInput.addEventListener('input', function() {
        updateBrokenLineColor("favorite-color", true);
        updateErrorIcon("favorite-color", true);

        setCriteriaPointIcon("favorite-color-picked", true);
        
        });
    }
});} catch (e) {
    console.error("Error attaching event listener:", e);
}            