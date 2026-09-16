/* =========================================================
   FOODREDISTRIBUTE
   FRONTEND JAVASCRIPT
   Flask API + JWT Authentication
   ========================================================= */


/* =========================================================
   CONFIGURATION
   ========================================================= */

window.API_BASE = window.API_BASE || "https://backend-bju0kn5g9-deepika-c083.vercel.app/api";


/* =========================================================
   LOCAL STORAGE HELPERS
   ========================================================= */

function getToken() {
    return localStorage.getItem("access_token");
}


function getLoggedInUser() {
    const user = localStorage.getItem("loggedInUser");

    if (!user) {
        return null;
    }

    try {
        return JSON.parse(user);
    } catch (error) {
        return null;
    }
}


function saveLoggedInUser(user) {
    localStorage.setItem(
        "loggedInUser",
        JSON.stringify(user)
    );
}


function clearSession() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("loggedInUser");
}


function logoutUser() {

    const token = getToken();

    /*
     * Tell backend about logout if possible.
     * Even if this fails, local session is cleared.
     */
    if (token) {
        fetch(API_BASE + "/auth/logout", {
            method: "POST",
            headers: {
                "Authorization": "Bearer " + token,
                "Content-Type": "application/json"
            }
        }).catch(function () {
            // Ignore logout API errors.
        });
    }

    clearSession();

    window.location.href = "login.html";
}


/* =========================================================
   GENERAL API REQUEST FUNCTION
   ========================================================= */

async function apiRequest(endpoint, options = {}) {

    const token = getToken();

    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {})
    };

    if (token) {
        headers["Authorization"] =
            "Bearer " + token;
    }

    try {

        const response = await fetch(API_BASE + endpoint, 
            {
                ...options,
                headers: headers
            }
        );

        let data = {};

        try {
            data = await response.json();
        } catch (error) {
            data = {};
        }


        /* =================================================
           IMPORTANT 401 FIX
           =================================================

           A 401 during LOGIN means wrong credentials.

           It does NOT mean that the user's existing
           session expired.

           Therefore we must NOT show the
           "session expired" popup for login.
        */

        if (response.status === 401) {

            if (endpoint === "/auth/login") {

                return {
                    ...data,
                    success: false,
                    status: 401
                };
            }


            /*
             * For protected pages, 401 really means
             * the token is invalid or expired.
             */

            clearSession();

            alert(
                "Your session has expired. Please login again."
            );

            window.location.href = "login.html";

            return null;
        }


        return {
            ...data,
            success:
                data.success !== undefined
                    ? data.success
                    : response.ok,
            status: response.status,
            ok: response.ok
        };

    } catch (error) {

        console.error(
            "API request error:",
            error
        );

        throw error;
    }
}


/* =========================================================
   LOGIN PROTECTION
   ========================================================= */

function requireLogin() {

    const token = getToken();
    const user = getLoggedInUser();

    if (!token || !user) {

        alert("Please login first.");

        window.location.href =
            "login.html";

        return false;
    }

    return true;
}


/* =========================================================
   HTML ESCAPE
   ========================================================= */

function escapeHTML(value) {

    if (value === null ||
        value === undefined) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function setDonationDefaults() {
    const quantityInput = document.getElementById("foodQuantity");
    if (quantityInput && (!quantityInput.value || Number.parseFloat(quantityInput.value) <= 0)) {
        quantityInput.value = "10";
    }

    const expiryInput = document.getElementById("foodExpiry");
    if (expiryInput && (!expiryInput.value || Number.isNaN(new Date(expiryInput.value).getTime()))) {
        const futureDate = new Date(Date.now() + 2 * 60 * 60 * 1000);
        expiryInput.value = futureDate.toISOString().slice(0, 16);
    }

    const foodTypeSelect = document.getElementById("foodType");
    if (foodTypeSelect && (!foodTypeSelect.value || !["cooked", "bakery", "fruits", "vegetables", "packaged"].includes(foodTypeSelect.value))) {
        foodTypeSelect.value = "cooked";
    }

    const priorityDonationAgeHours = document.getElementById("priorityDonationAgeHours");
    if (priorityDonationAgeHours && (!priorityDonationAgeHours.value || Number(priorityDonationAgeHours.value) <= 0)) {
        priorityDonationAgeHours.value = "1";
    }

    const priorityStorageCondition = document.getElementById("priorityStorageCondition");
    if (priorityStorageCondition && !priorityStorageCondition.value) {
        priorityStorageCondition.value = "refrigerated";
    }

    const priorityFoodCategory = document.getElementById("priorityFoodCategory");
    if (priorityFoodCategory && !priorityFoodCategory.value) {
        priorityFoodCategory.value = "non_vegetarian";
    }
}

document.addEventListener("DOMContentLoaded", function () {
    setDonationDefaults();
});


/* =========================================================
   FORMAT DATE
   ========================================================= */

function formatDate(value) {

    if (!value) {
        return "-";
    }

    try {

        return new Date(value)
            .toLocaleString();

    } catch (error) {

        return value;
    }
}


/* =========================================================
   NORMALIZE ROLE
   ========================================================= */

function normalizeRole(role) {

    const normalized = String(role || "")
        .trim()
        .toLowerCase();

    if (normalized === "individual") {
        return "donor";
    }

    return normalized;
}


function formatConfidence(value) {
    if (value === null || value === undefined || value === "") {
        return "-";
    }

    const numeric = Number(value);

    if (Number.isNaN(numeric)) {
        return "-";
    }

    if (numeric <= 1) {
        return `${(numeric * 100).toFixed(1)}%`;
    }

    return `${Math.min(numeric, 100).toFixed(1)}%`;
}


function getPriorityBadgeClass(priority) {
    const value = String(priority || "").trim();

    if (value.toLowerCase() === "critical") {
        return "priority-critical";
    }
    if (value.toLowerCase() === "high") {
        return "priority-high";
    }
    if (value.toLowerCase() === "medium") {
        return "priority-medium";
    }
    if (value.toLowerCase() === "low") {
        return "priority-low";
    }

    return "priority-low";
}

function setPriorityBadge(priority) {
    const value = String(priority || "").trim();
    const element = document.getElementById("foodPriorityValue");

    if (!element) {
        return;
    }

    element.className = "priority-value";
    element.classList.add(getPriorityBadgeClass(value));
    element.textContent = value || "-";
}


/* =========================================================
   REDIRECT USER
   ========================================================= */

function redirectUser(user) {

    const role =
        normalizeRole(user.role);

    if (role === "ngo") {

        window.location.href =
            "ngo_dashboard.html";

    } else if (role === "admin") {

        window.location.href =
            "admin.html";

    } else if (role === "volunteer") {

        window.location.href =
            "volunteer.html";

    } else {

        window.location.href =
            "dashboard.html";
    }
}


/* =========================================================
   REGISTER
   ========================================================= */

const registerForm =
    document.getElementById("registerForm");


if (registerForm) {

    registerForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            const nameElement =
                document.getElementById("fullName");

            const emailElement =
                document.getElementById("registerEmail");

            const phoneElement =
                document.getElementById("registerPhone");

            const roleElement =
                document.getElementById("accountType");

            const passwordElement =
                document.getElementById(
                    "registerPassword"
                );

            const confirmPasswordElement =
                document.getElementById(
                    "confirmPassword"
                );

            const addressElement =
                document.getElementById(
                    "registerAddress"
                );

            const cityElement =
                document.getElementById(
                    "registerCity"
                );

            const pincodeElement =
                document.getElementById(
                    "registerPincode"
                );

            const message =
                document.getElementById(
                    "registerMessage"
                );


            const name =
                nameElement
                    ? nameElement.value.trim()
                    : "";

            const email =
                emailElement
                    ? emailElement.value.trim()
                    : "";

            const phone =
                phoneElement
                    ? phoneElement.value.trim()
                    : "";

            const role =
                roleElement
                    ? roleElement.value
                    : "";

            const password =
                passwordElement
                    ? passwordElement.value
                    : "";

            const confirmPassword =
                confirmPasswordElement
                    ? confirmPasswordElement.value
                    : "";

            const address =
                addressElement
                    ? addressElement.value.trim()
                    : "";

            const city =
                cityElement
                    ? cityElement.value.trim()
                    : "";

            const pincode =
                pincodeElement
                    ? pincodeElement.value.trim()
                    : "";


            /* Validation */

            if (!name) {

                message.textContent =
                    "❌ Please enter your name.";

                message.style.color =
                    "#d32f2f";

                return;
            }


            if (!email) {

                message.textContent =
                    "❌ Please enter your email.";

                message.style.color =
                    "#d32f2f";

                return;
            }


            if (!role) {

                message.textContent =
                    "❌ Please select an account type.";

                message.style.color =
                    "#d32f2f";

                return;
            }


            if (!password) {

                message.textContent =
                    "❌ Please enter a password.";

                message.style.color =
                    "#d32f2f";

                return;
            }


            if (password.length < 6) {

                message.textContent =
                    "❌ Password must contain at least 6 characters.";

                message.style.color =
                    "#d32f2f";

                return;
            }


            if (password !== confirmPassword) {

                message.textContent =
                    "❌ Passwords do not match.";

                message.style.color =
                    "#d32f2f";

                return;
            }


            message.textContent =
                "⏳ Creating account...";

            message.style.color =
                "#2e7d32";


            try {

                /*
                 * Send registration to Flask.
                 */

                const result =
                    await apiRequest(
                        "/auth/register",
                        {
                            method: "POST",

                            body: JSON.stringify({
                                name: name,
                                email: email,
                                password: password,
                                role: normalizeRole(role),
                                phone: phone,
                                address: address,
                                city: city,
                                pincode: pincode
                            })
                        }
                    );


                if (!result) {
                    return;
                }


                if (
                    !result.ok &&
                    !result.success
                ) {

                    const errorMessage =
                        result.error ||
                        result.message ||
                        result.detail ||
                        "Registration failed.";

                    message.textContent =
                        "❌ " + errorMessage;

                    message.style.color =
                        "#d32f2f";

                    return;
                }


                message.textContent =
                    "✅ Account created successfully! Redirecting to login...";

                message.style.color =
                    "#2e7d32";


                registerForm.reset();


                setTimeout(
                    function () {

                        window.location.href =
                            "login.html";

                    },
                    1200
                );


            } catch (error) {

                console.error(
                    "Registration error:",
                    error
                );

                message.textContent =
                    "❌ Cannot connect to backend. Make sure Flask is running.";

                message.style.color =
                    "#d32f2f";
            }
        }
    );
}


/* =========================================================
   LOGIN
   ========================================================= */

const loginForm =
    document.getElementById("loginForm");


if (loginForm) {

    loginForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const roleElement =
                document.getElementById(
                    "userRole"
                );

            const emailElement =
                document.getElementById(
                    "loginEmail"
                );

            const passwordElement =
                document.getElementById(
                    "loginPassword"
                );

            const message =
                document.getElementById(
                    "loginMessage"
                );


            const role =
                roleElement
                    ? normalizeRole(
                        roleElement.value
                    )
                    : "";

            const email =
                emailElement
                    ? emailElement.value.trim()
                    : "";

            const password =
                passwordElement
                    ? passwordElement.value
                    : "";


            if (!email) {

                message.textContent =
                    "❌ Please enter your email.";

                message.style.color =
                    "#d32f2f";

                return;
            }


            if (!password) {

                message.textContent =
                    "❌ Please enter your password.";

                message.style.color =
                    "#d32f2f";

                return;
            }


            message.textContent =
                "⏳ Logging in...";

            message.style.color =
                "#2e7d32";


            /*
             * Remove old token before attempting
             * a completely new login.
             */

            localStorage.removeItem(
                "access_token"
            );

            localStorage.removeItem(
                "loggedInUser"
            );


            try {

                const result =
                    await apiRequest(
                        "/auth/login",
                        {
                            method: "POST",

                            body: JSON.stringify({
                                email: email,
                                password: password
                            })
                        }
                    );


                console.log(
                    "Login response:",
                    result
                );


                if (!result) {
                    return;
                }


                /*
                 * IMPORTANT:
                 *
                 * Do not use:
                 *
                 * if (result.status === 401)
                 *
                 * to show "session expired".
                 *
                 * Login 401 means incorrect credentials.
                 */


                if (
                    result.status === 401 ||
                    result.success === false ||
                    result.ok === false
                ) {

                    const errorMessage =
                        result.error ||
                        result.message ||
                        result.detail ||
                        "Invalid email or password.";

                    message.textContent =
                        "❌ " + errorMessage;

                    message.style.color =
                        "#d32f2f";

                    return;
                }


                /*
                 * Backend normally returns:
                 *
                 * access_token
                 * user
                 *
                 * Handle both normal and nested
                 * response formats.
                 */

                const token =
                    result.access_token ||
                    result.token;


                let user =
                    result.user ||
                    result.data ||
                    null;


                /*
                 * If backend returns user fields
                 * directly, create the user object.
                 */

                if (!user && result.user_id) {

                    user = {
                        id: result.user_id,
                        name: result.name,
                        email: email,
                        role: result.role,
                        location: result.location
                    };
                }


                if (!token) {

                    message.textContent =
                        "❌ Login response did not contain an access token.";

                    message.style.color =
                        "#d32f2f";

                    console.error(
                        "Missing access token:",
                        result
                    );

                    return;
                }


                if (!user) {

                    message.textContent =
                        "❌ Login response did not contain user information.";

                    message.style.color =
                        "#d32f2f";

                    console.error(
                        "Missing user:",
                        result
                    );

                    return;
                }


                /*
                 * Check selected role.
                 */

                const backendRole =
                    normalizeRole(user.role);


                if (
                    role &&
                    role !== backendRole
                ) {

                    message.textContent =
                        "ℹ️ Selected role does not match the account. Logging in with the account role instead...";

                    message.style.color =
                        "#2e7d32";
                }


                /*
                 * Save login session.
                 */

                localStorage.setItem(
                    "access_token",
                    token
                );

                saveLoggedInUser(user);


                message.textContent =
                    "✅ Login successful! Redirecting...";

                message.style.color =
                    "#2e7d32";


                setTimeout(
                    function () {

                        redirectUser(user);

                    },
                    700
                );


            } catch (error) {

                console.error(
                    "Login error:",
                    error
                );

                message.textContent =
                    "❌ Cannot connect to backend. Make sure Flask is running.";

                message.style.color =
                    "#d32f2f";
            }
        }
    );
}


/* =========================================================
   FOOD PRIORITY PREDICTION
   ========================================================= */

const foodPriorityForm = document.getElementById("foodPriorityForm");

if (foodPriorityForm) {
    foodPriorityForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const expiryHoursElement = document.getElementById("expiryHours");
        const quantityElement = document.getElementById("quantity");
        const foodTypeElement = document.getElementById("foodType");
        const donationAgeHoursElement = document.getElementById("donationAgeHours");
        const storageConditionElement = document.getElementById("storageCondition");
        const foodCategoryElement = document.getElementById("foodCategory");
        const errorElement = document.getElementById("foodPriorityError");
        const resultElement = document.getElementById("foodPriorityResult");
        const priorityElement = document.getElementById("foodPriorityValue");
        const confidenceElement = document.getElementById("foodPriorityConfidence");
        const messageElement = document.getElementById("foodPriorityMessage");

        if (errorElement) {
            errorElement.textContent = "";
            errorElement.style.display = "none";
        }

        if (resultElement) {
            resultElement.classList.add("hidden");
        }

        const payload = {
            expiry_hours: expiryHoursElement ? Number(expiryHoursElement.value) : NaN,
            quantity: quantityElement ? Number(quantityElement.value) : NaN,
            food_type: foodTypeElement ? foodTypeElement.value.trim() : "",
            donation_age_hours: donationAgeHoursElement ? Number(donationAgeHoursElement.value) : NaN,
            storage_condition: storageConditionElement ? storageConditionElement.value.trim() : "",
            food_category: foodCategoryElement ? foodCategoryElement.value.trim() : ""
        };

        if (
            !Number.isFinite(payload.expiry_hours) ||
            payload.expiry_hours < 0 ||
            !Number.isFinite(payload.quantity) ||
            payload.quantity < 0 ||
            !Number.isFinite(payload.donation_age_hours) ||
            payload.donation_age_hours < 0 ||
            !payload.food_type ||
            !payload.storage_condition ||
            !payload.food_category
        ) {
            if (errorElement) {
                errorElement.textContent = "Please enter valid values for all six fields before predicting.";
                errorElement.style.display = "block";
            }
            return;
        }

        try {
            const response = await fetch(API_BASE + "/food-priority/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json().catch(() => ({}));

            if (!response.ok || !data || data.success !== true) {
                const errorText = data && (data.error || data.message) ? (data.error || data.message) : "Prediction failed. Please check your values and try again.";

                if (errorElement) {
                    errorElement.textContent = errorText;
                    errorElement.style.display = "block";
                }

                if (resultElement) {
                    resultElement.classList.add("hidden");
                }
                return;
            }

            const predictedPriority = data.priority || "-";
            const confidenceValue = data.confidence;

            if (priorityElement) {
                priorityElement.textContent = predictedPriority;
                setPriorityBadge(predictedPriority);
            }

            if (confidenceElement) {
                confidenceElement.textContent = formatConfidence(confidenceValue);
            }

            if (messageElement) {
                messageElement.textContent = `Food priority is assessed as ${predictedPriority}.`;
            }

            if (resultElement) {
                resultElement.classList.remove("hidden");
            }

        } catch (error) {
            console.error("Food priority prediction error:", error);

            if (errorElement) {
                errorElement.textContent = "Unable to contact the prediction API. Please make sure the Flask backend is running on port 5000.";
                errorElement.style.display = "block";
            }
        }
    });
}


/* =========================================================
   FOOD PRIORITY PREDICTION
   ========================================================= */

const predictPriorityButton = document.getElementById("predictPriorityButton");

function getPriorityAnalysisContext() {
    const foodExpiryInput = document.getElementById("foodExpiry");
    const foodQuantityInput = document.getElementById("foodQuantity");
    const foodTypeSelect = document.getElementById("foodType");
    const storageConditionInput = document.getElementById("priorityStorageCondition");
    const foodCategoryInput = document.getElementById("priorityFoodCategory");

    const expiryDate = foodExpiryInput && foodExpiryInput.value ? new Date(foodExpiryInput.value) : null;
    const expiryHours = expiryDate && !Number.isNaN(expiryDate.getTime())
        ? Math.max(0, (expiryDate.getTime() - Date.now()) / (1000 * 60 * 60))
        : 0;

    const quantityValue = Number((foodQuantityInput?.value || "0").toString().replace(/[^0-9.\-]/g, ""));
    const foodType = (foodTypeSelect?.value || "").trim();
    const storageCondition = storageConditionInput?.value || "refrigerated";
    const foodCategory = foodCategoryInput?.value || "non_vegetarian";
    const donationAgeHours = Math.max(0, Math.min(72, expiryHours > 0 ? Math.max(1, Math.round(Math.max(0, 24 - expiryHours))) : 1));

    return {
        expiryDate,
        expiryHours,
        quantityValue,
        foodType,
        storageCondition,
        foodCategory,
        donationAgeHours
    };
}

function setPriorityStatusUI(priority, confidence, probabilities = {}) {
    const valueElement = document.getElementById("priorityResultValue");
    const confidenceElement = document.getElementById("priorityResultConfidence");
    const detailsElement = document.getElementById("priorityResultDetails");

    if (valueElement) {
        valueElement.textContent = priority || "-";
        valueElement.className = "priority-badge neutral";

        if (priority === "Critical") valueElement.classList.add("priority-critical");
        else if (priority === "High") valueElement.classList.add("priority-high");
        else if (priority === "Medium") valueElement.classList.add("priority-medium");
        else if (priority === "Low") valueElement.classList.add("priority-low");
    }

    if (confidenceElement) {
        const numericConfidence = Number(confidence);
        confidenceElement.textContent = Number.isFinite(numericConfidence)
            ? (numericConfidence <= 1 ? `${(numericConfidence * 100).toFixed(1)}%` : `${numericConfidence.toFixed(1)}%`)
            : "-";
    }

    const detailText = {
        Critical: "Immediate redistribution is recommended because this donation is likely to expire or spoil soon.",
        High: "This donation needs early dispatch and attention to prevent food loss and spoilage.",
        Medium: "This donation should be prioritized soon but can be scheduled within the next wave of operations.",
        Low: "This donation has a healthier time window and can be handled as part of a routine redistribution cycle."
    };

    if (detailsElement) {
        detailsElement.textContent = detailText[priority] || "Priority is being evaluated based on donation urgency.";
    }

    ["Critical", "High", "Medium", "Low"].forEach((level) => {
        const element = document.getElementById(`prob${level}`);
        if (element) {
            const value = probabilities && probabilities[level] !== undefined ? probabilities[level] : 0;
            element.textContent = `${(Number(value) * 100).toFixed(1)}%`;
        }
    });
}

if (predictPriorityButton) {
    predictPriorityButton.addEventListener("click", async function () {
        const foodExpiryInput = document.getElementById("foodExpiry");
        const foodQuantityInput = document.getElementById("foodQuantity");
        const foodTypeSelect = document.getElementById("foodType");
        const storageConditionInput = document.getElementById("priorityStorageCondition");
        const foodCategoryInput = document.getElementById("priorityFoodCategory");
        const errorElement = document.getElementById("priorityPredictionError");
        const resultElement = document.getElementById("priorityPredictionResult");

        if (!foodExpiryInput || !foodQuantityInput || !foodTypeSelect) {
            if (errorElement) {
                errorElement.textContent = "Donation form fields are missing. Please refresh the page.";
                errorElement.style.display = "block";
            }
            return;
        }

        if (!foodExpiryInput.value || Number.isNaN(new Date(foodExpiryInput.value).getTime())) {
            const futureDate = new Date(Date.now() + 2 * 60 * 60 * 1000);
            foodExpiryInput.value = futureDate.toISOString().slice(0, 16);
        }

        if (!foodQuantityInput.value || Number.parseFloat(foodQuantityInput.value) <= 0) {
            foodQuantityInput.value = "10";
        }

        if (!foodTypeSelect.value || !["cooked", "bakery", "fruits", "vegetables", "packaged"].includes(foodTypeSelect.value)) {
            foodTypeSelect.value = "cooked";
        }

        if (!storageConditionInput || !storageConditionInput.value) {
            if (storageConditionInput) storageConditionInput.value = "refrigerated";
        }

        if (!foodCategoryInput || !foodCategoryInput.value) {
            if (foodCategoryInput) foodCategoryInput.value = "non_vegetarian";
        }

        const context = getPriorityAnalysisContext();
        const analysisExpiryLabel = document.getElementById("analysisExpiryLabel");
        const analysisQuantityLabel = document.getElementById("analysisQuantityLabel");
        const analysisFoodTypeLabel = document.getElementById("analysisFoodTypeLabel");

        if (analysisExpiryLabel) {
            const expiryText = context.expiryDate ? `${context.expiryHours.toFixed(1)} hrs` : "Not set";
            analysisExpiryLabel.textContent = expiryText;
        }

        if (analysisQuantityLabel) {
            analysisQuantityLabel.textContent = Number.isFinite(context.quantityValue) ? `${context.quantityValue} kg` : "--";
        }

        if (analysisFoodTypeLabel) {
            analysisFoodTypeLabel.textContent = context.foodType || "Unspecified";
        }

        if (errorElement) {
            errorElement.style.display = "none";
            errorElement.textContent = "";
        }

        if (resultElement) {
            resultElement.classList.add("hidden");
        }

        if (
            !Number.isFinite(context.expiryHours) || context.expiryHours < 0 ||
            !Number.isFinite(context.quantityValue) || context.quantityValue <= 0 ||
            !context.foodType ||
            !context.storageCondition ||
            !context.foodCategory
        ) {
            if (errorElement) {
                errorElement.textContent = "Please complete the donation form before running the priority analysis.";
                errorElement.style.display = "block";
            }
            return;
        }

        const payload = {
            expiry_hours: Number(context.expiryHours.toFixed(2)),
            quantity: Number(context.quantityValue),
            food_type: context.foodType,
            donation_age_hours: Number(context.donationAgeHours),
            storage_condition: context.storageCondition,
            food_category: context.foodCategory
        };

        try {
            const response = await fetch(API_BASE + "/food-priority/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json().catch(() => ({}));

            if (!response.ok || !data || data.success !== true) {
                const message = data && (data.error || data.message) ? (data.error || data.message) : "Prediction failed.";

                if (errorElement) {
                    errorElement.textContent = message;
                    errorElement.style.display = "block";
                }
                return;
            }

            const priority = data.priority || "-";
            const confidence = data.confidence;
            const probabilities = data.probabilities || {};

            setPriorityStatusUI(priority, confidence, probabilities);

            if (resultElement) {
                resultElement.classList.remove("hidden");
            }
        } catch (error) {
            console.error("Food priority prediction error:", error);

            if (errorElement) {
                errorElement.textContent = "Unable to connect to the Flask API. Make sure the backend is running on port 5000.";
                errorElement.style.display = "block";
            }
        }
    });
}


/* =========================================================
   DONATE FOOD
   ========================================================= */

const donateForm =
    document.getElementById("donateForm") ||
    document.getElementById("donationForm");


if (donateForm) {

    donateForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            if (!requireLogin()) {
                return;
            }


            const user =
                getLoggedInUser();


            const foodNameElement =
                document.getElementById("foodName") ||
                document.getElementById("food_name");

            const foodTypeElement =
                document.getElementById("foodType") ||
                document.getElementById("food_type");

            const quantityElement =
                document.getElementById("foodQuantity") ||
                document.getElementById("quantity");

            const locationElement =
                document.getElementById("foodLocation") ||
                document.getElementById("location");

            const expiryElement =
                document.getElementById("foodExpiry") ||
                document.getElementById("expiry_time");

            const servingsElement =
                document.getElementById(
                    "servings"
                );

            const priorityDonationAgeHoursElement =
                document.getElementById("priorityDonationAgeHours");

            const priorityStorageConditionElement =
                document.getElementById("priorityStorageCondition") ||
                document.getElementById("storage_condition");

            const priorityFoodCategoryElement =
                document.getElementById("priorityFoodCategory");


            if (!foodNameElement ||
                !quantityElement ||
                !locationElement ||
                !expiryElement) {

                alert(
                    "Some donation form fields are missing."
                );

                return;
            }


            const foodName =
                foodNameElement.value.trim();

            const foodType =
                foodTypeElement
                    ? foodTypeElement.value.trim()
                    : "";

            const quantity =
                parseFloat(
                    quantityElement.value
                );

            const location =
                locationElement.value.trim();

            const expiry =
                expiryElement.value;

            const expiryHours =
                (new Date(expiry).getTime() - Date.now()) / (1000 * 60 * 60);

            const donationAgeHours =
                priorityDonationAgeHoursElement && priorityDonationAgeHoursElement.value
                    ? Number(priorityDonationAgeHoursElement.value)
                    : Math.max(0, Number((24 - expiryHours).toFixed(2)));

            const servings =
                servingsElement
                    ? parseInt(
                        servingsElement.value
                    ) || null
                    : null;


            if (!foodName) {

                alert(
                    "Please enter food name."
                );

                return;
            }


            if (
                isNaN(quantity) ||
                quantity <= 0
            ) {

                alert(
                    "Please enter a valid quantity."
                );

                return;
            }


            if (!location) {

                alert(
                    "Please enter pickup location."
                );

                return;
            }


            if (!expiry) {

                alert(
                    "Please enter expiry time."
                );

                return;
            }


            try {

                const result =
                    await apiRequest(
                        "/donations",
                        {
                            method: "POST",

                            body: JSON.stringify({
                                food_name:
                                    foodName,

                                food_type:
                                    foodType,

                                quantity:
                                    quantity,

                                unit:
                                    "kg",

                                servings:
                                    servings,

                                pickup_location:
                                    location,

                                expiry_time:
                                    expiry,

                                expiry_hours:
                                    Number(expiryHours.toFixed(2)),

                                storage_condition:
                                    priorityStorageConditionElement && priorityStorageConditionElement.value
                                        ? priorityStorageConditionElement.value
                                        : "room_temperature",

                                food_category:
                                    priorityFoodCategoryElement && priorityFoodCategoryElement.value
                                        ? priorityFoodCategoryElement.value
                                        : "unknown",

                                donation_age_hours:
                                    donationAgeHours
                            })
                        }
                    );


                if (!result) {
                    return;
                }


                if (
                    !result.ok &&
                    !result.success
                ) {

                    alert(
                        "❌ " +
                        (
                            result.error ||
                            result.message ||
                            result.detail ||
                            "Donation failed."
                        )
                    );

                    return;
                }


                alert(
                    "✅ Food donation submitted successfully!"
                );


                donateForm.reset();


                window.location.href =
                    "dashboard.html";


            } catch (error) {

                console.error(
                    "Donation error:",
                    error
                );

                alert(
                    "❌ Could not submit donation. Check that Flask is running."
                );
            }
        }
    );
}


/* =========================================================
   DONOR DASHBOARD
   ========================================================= */

async function loadDonorDashboard() {

    if (!requireLogin()) {
        return;
    }


    const user =
        getLoggedInUser();


    try {

        const result =
            await apiRequest(
                "/donations/my",
                {
                    method: "GET"
                }
            );


        if (!result) {
            return;
        }


        if (
            !result.ok &&
            !result.success
        ) {

            console.error(
                "Could not load donations:",
                result
            );

            return;
        }


        const donations =
            Array.isArray(result)
                ? result
                : (
                    result.donations ||
                    result.data ||
                    []
                );


        displayBackendDonations(
            donations
        );

        updateDonorStatisticsBackend(
            donations
        );


        const nameElements =
            document.querySelectorAll(
                ".dashboard-profile strong, .user-name"
            );


        nameElements.forEach(
            function (element) {

                if (user && user.name) {

                    element.textContent =
                        user.name;
                }
            }
        );


    } catch (error) {

        console.error(
            "Dashboard error:",
            error
        );
    }
}


/* =========================================================
   DISPLAY DONOR DONATIONS
   ========================================================= */

function displayBackendDonations(
    donations
) {

    const tableBody =
        document.getElementById(
            "donationList"
        );


    if (!tableBody) {
        return;
    }


    tableBody.innerHTML = "";


    if (
        !Array.isArray(donations) ||
        donations.length === 0
    ) {

        tableBody.innerHTML = `
            <tr>
                <td colspan="6"
                    style="text-align:center;">
                    No donations yet.
                </td>
            </tr>
        `;

        return;
    }


    donations.forEach(
        function (donation) {

            const row =
                document.createElement(
                    "tr"
                );


            row.innerHTML = `
                <td>
                    🍱
                    ${escapeHTML(
                        donation.food_name
                    )}
                </td>

                <td>
                    ${escapeHTML(
                        donation.quantity
                    )}
                    ${escapeHTML(
                        donation.unit || "kg"
                    )}
                </td>

                <td>
                    ${escapeHTML(
                        donation.pickup_location ||
                        "-"
                    )}
                </td>

                <td>
                    ${formatDate(
                        donation.expiry_time
                    )}
                </td>

                <td>
                    <span class="status pending">
                        ${escapeHTML(
                            donation.status ||
                            "AVAILABLE"
                        )}
                    </span>
                </td>

                <td>
                    ${formatDate(
                        donation.created_at
                    )}
                </td>
            `;


            tableBody.appendChild(
                row
            );
        }
    );
}


/* =========================================================
   DONOR STATISTICS
   ========================================================= */

function updateDonorStatisticsBackend(
    donations
) {

    if (!Array.isArray(donations)) {
        return;
    }


    let totalMeals = 0;

    let totalFood = 0;


    donations.forEach(
        function (donation) {

            totalMeals +=
                Number(
                    donation.servings
                ) || 0;

            totalFood +=
                Number(
                    donation.quantity
                ) || 0;
        }
    );


    const cards =
        document.querySelectorAll(
            ".dashboard-stat-card"
        );


    if (!cards.length) {
        return;
    }


    if (cards[0]) {

        const value =
            cards[0].querySelector(
                "strong"
            );

        if (value) {
            value.textContent =
                donations.length;
        }
    }


    if (cards[1]) {

        const value =
            cards[1].querySelector(
                "strong"
            );

        if (value) {
            value.textContent =
                totalMeals;
        }
    }


    if (cards[2]) {

        const value =
            cards[2].querySelector(
                "strong"
            );

        if (value) {
            value.textContent =
                totalMeals;
        }
    }


    if (cards[3]) {

        const value =
            cards[3].querySelector(
                "strong"
            );

        if (value) {

            value.textContent =
                totalFood.toFixed(1) +
                " kg";
        }
    }
}


/* =========================================================
   NGO AVAILABLE DONATIONS
   ========================================================= */

async function loadNGOAvailableFood() {

    if (!requireLogin()) {
        return;
    }


    try {

        const result =
            await apiRequest(
                "/ngo/available-donations",
                {
                    method: "GET"
                }
            );


        if (!result) {
            return;
        }


        const donations =
            Array.isArray(result)
                ? result
                : (
                    result.donations ||
                    result.data ||
                    []
                );


        displayNGOAvailableFood(
            donations
        );


    } catch (error) {

        console.error(
            "NGO available food error:",
            error
        );
    }
}


/* =========================================================
   DISPLAY NGO AVAILABLE FOOD
   ========================================================= */

function displayNGOAvailableFood(
    donations
) {

    const tableBody =
        document.getElementById(
            "availableFoodList"
        );


    if (!tableBody) {
        return;
    }


    tableBody.innerHTML = "";


    if (
        !Array.isArray(donations) ||
        donations.length === 0
    ) {

        tableBody.innerHTML = `
            <tr>
                <td colspan="6"
                    style="text-align:center;">
                    No food donations are currently available.
                </td>
            </tr>
        `;

        return;
    }


    donations.forEach(
        function (donation) {

            const row =
                document.createElement(
                    "tr"
                );

            const priorityValue = String(donation.priority || "Low").trim();
            const priorityClass = getPriorityBadgeClass(priorityValue);

            row.innerHTML = `
                <td>
                    🍱
                    ${escapeHTML(
                        donation.food_name
                    )}
                </td>

                <td>
                    <span class="priority-badge ${priorityClass}">
                        ${escapeHTML(priorityValue)}
                    </span>
                </td>

                <td>
                    ${escapeHTML(
                        donation.quantity
                    )}
                    ${escapeHTML(
                        donation.unit ||
                        "kg"
                    )}
                </td>

                <td>
                    ${escapeHTML(
                        donation.pickup_location ||
                        "-"
                    )}
                </td>

                <td>
                    ${formatDate(
                        donation.expiry_time
                    )}
                </td>

                <td>
                    <button
                        class="accept-button"
                        onclick="acceptDonation(${donation.id})">
                        Accept
                    </button>
                </td>
            `;


            tableBody.appendChild(
                row
            );
        }
    );
}


/* =========================================================
   NGO ACCEPT DONATION
   ========================================================= */

async function acceptDonation(
    donationId
) {

    if (!requireLogin()) {
        return;
    }


    const confirmed =
        confirm(
            "Do you want to accept this food donation?"
        );


    if (!confirmed) {
        return;
    }


    try {

        const result =
            await apiRequest(
                "/ngo/claim/" +
                donationId,
                {
                    method: "POST",

                    body: JSON.stringify({})
                }
            );


        if (!result) {
            return;
        }


        if (
            !result.ok &&
            !result.success
        ) {

            alert(
                "❌ " +
                (
                    result.error ||
                    result.message ||
                    result.detail ||
                    "Could not accept donation."
                )
            );

            return;
        }


        alert(
            "✅ Donation accepted successfully!"
        );


        loadNGOAvailableFood();


        if (
            typeof displayNGORequests ===
            "function"
        ) {

            displayNGORequests();
        }


        if (
            typeof updateNGOStatistics ===
            "function"
        ) {

            updateNGOStatistics();
        }


    } catch (error) {

        console.error(
            "Accept donation error:",
            error
        );

        alert(
            "❌ Could not connect to backend."
        );
    }
}


/* =========================================================
   NGO CLAIMS
   ========================================================= */

async function loadNGOClaims() {

    if (!requireLogin()) {
        return;
    }


    try {

        const result =
            await apiRequest(
                "/ngo/claims",
                {
                    method: "GET"
                }
            );


        if (!result) {
            return;
        }


        const claims =
            Array.isArray(result)
                ? result
                : (
                    result.claims ||
                    result.data ||
                    []
                );


        displayNGOClaims(
            claims
        );


    } catch (error) {

        console.error(
            "NGO claims error:",
            error
        );
    }
}


/* =========================================================
   DISPLAY NGO CLAIMS
   ========================================================= */

function displayNGOClaims(
    claims
) {

    const tableBody =
        document.getElementById(
            "ngoRequestList"
        );


    if (!tableBody) {
        return;
    }


    tableBody.innerHTML = "";


    if (
        !Array.isArray(claims) ||
        claims.length === 0
    ) {

        tableBody.innerHTML = `
            <tr>
                <td colspan="6"
                    style="text-align:center;">
                    No claims yet.
                </td>
            </tr>
        `;

        return;
    }


    claims.forEach(
        function (claim) {

            const row =
                document.createElement(
                    "tr"
                );


            row.innerHTML = `
                <td>
                    #${escapeHTML(
                        claim.id
                    )}
                </td>

                <td>
                    🍱 Donation #
                    ${escapeHTML(
                        claim.donation_id
                    )}
                </td>

                <td>
                    NGO #
                    ${escapeHTML(
                        claim.ngo_id
                    )}
                </td>

                <td>
                    <span class="status delivered">
                        ${escapeHTML(
                            claim.status ||
                            "ACCEPTED"
                        )}
                    </span>
                </td>

                <td>
                    ${formatDate(
                        claim.claimed_at
                    )}
                </td>
            `;


            tableBody.appendChild(
                row
            );
        }
    );
}


/* =========================================================
   NGO FOOD REQUEST
   ========================================================= */

const foodRequestForm =
    document.getElementById(
        "foodRequestForm"
    );


if (foodRequestForm) {

    foodRequestForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            if (!requireLogin()) {
                return;
            }


            const foodElement =
                document.getElementById(
                    "requiredFood"
                );

            const quantityElement =
                document.getElementById(
                    "requiredQuantity"
                );

            const servingsElement =
                document.getElementById(
                    "requiredServings"
                );

            const urgencyElement =
                document.getElementById(
                    "urgency"
                );

            const message =
                document.getElementById(
                    "requestMessage"
                );


            const foodType =
                foodElement
                    ? foodElement.value.trim()
                    : "";

            const quantity =
                quantityElement
                    ? parseFloat(
                        quantityElement.value
                    )
                    : NaN;

            const servings =
                servingsElement
                    ? parseInt(
                        servingsElement.value
                    ) || null
                    : null;

            const urgency =
                urgencyElement
                    ? urgencyElement.value
                    : "NORMAL";


            if (!foodType) {

                message.textContent =
                    "❌ Please enter required food.";

                message.style.color =
                    "#d32f2f";

                return;
            }


            if (
                isNaN(quantity) ||
                quantity <= 0
            ) {

                message.textContent =
                    "❌ Please enter a valid quantity.";

                message.style.color =
                    "#d32f2f";

                return;
            }


            try {

                const result =
                    await apiRequest(
                        "/ngo/food-request",
                        {
                            method: "POST",

                            body: JSON.stringify({
                                food_type:
                                    foodType,

                                quantity_required:
                                    quantity,

                                servings_required:
                                    servings,

                                urgency:
                                    urgency
                            })
                        }
                    );


                if (!result) {
                    return;
                }


                if (
                    !result.ok &&
                    !result.success
                ) {

                    message.textContent =
                        "❌ " +
                        (
                            result.error ||
                            result.message ||
                            result.detail ||
                            "Request failed."
                        );

                    message.style.color =
                        "#d32f2f";

                    return;
                }


                message.textContent =
                    "✅ Food request submitted successfully.";

                message.style.color =
                    "#2e7d32";


                foodRequestForm.reset();


            } catch (error) {

                console.error(
                    "Food request error:",
                    error
                );

                message.textContent =
                    "❌ Could not connect to backend.";

                message.style.color =
                    "#d32f2f";
            }
        }
    );
}


/* =========================================================
   NGO FOOD REQUESTS
   ========================================================= */

async function loadNGOFoodRequests() {

    if (!requireLogin()) {
        return;
    }


    try {

        const result =
            await apiRequest(
                "/ngo/food-requests",
                {
                    method: "GET"
                }
            );


        if (!result) {
            return;
        }


        console.log(
            "NGO food requests:",
            result
        );


    } catch (error) {

        console.error(
            "Food requests error:",
            error
        );
    }
}


/* =========================================================
   NEED FOOD PAGE
   ========================================================= */

async function loadNeedFood() {

    try {

        const result =
            await apiRequest(
                "/ngo/available-donations",
                {
                    method: "GET"
                }
            );


        if (!result) {
            return;
        }


        const donations =
            Array.isArray(result)
                ? result
                : (
                    result.donations ||
                    result.data ||
                    []
                );


        displayNeedFoodBackend(
            donations
        );


    } catch (error) {

        console.error(
            "Need food error:",
            error
        );
    }
}


/* =========================================================
   DISPLAY NEED FOOD
   ========================================================= */

function displayNeedFoodBackend(
    donations
) {

    const container =
        document.getElementById(
            "needFoodList"
        );


    if (!container) {
        return;
    }


    container.innerHTML = "";


    if (
        !Array.isArray(donations) ||
        donations.length === 0
    ) {

        container.innerHTML = `
            <div class="no-food-message">
                <div>🍱</div>

                <h3>
                    No food available right now
                </h3>

                <p>
                    New surplus food donations
                    will appear here when available.
                </p>
            </div>
        `;

        return;
    }


    donations.forEach(
        function (donation) {

            const card =
                document.createElement(
                    "div"
                );


            card.className =
                "available-food-card";


            card.innerHTML = `
                <div class="food-card-icon">
                    🍱
                </div>

                <span class="food-status">
                    ● Available
                </span>

                <h3>
                    ${escapeHTML(
                        donation.food_name
                    )}
                </h3>

                <p>
                    🍽️
                    ${escapeHTML(
                        donation.quantity
                    )}
                    ${escapeHTML(
                        donation.unit ||
                        "kg"
                    )}
                </p>

                <p>
                    📍
                    ${escapeHTML(
                        donation.pickup_location ||
                        "-"
                    )}
                </p>

                <p>
                    ⏰ Best before:
                    ${formatDate(
                        donation.expiry_time
                    )}
                </p>

                <button
                    class="food-request-button"
                    onclick="requestAvailableFood(${donation.id})">
                    Request This Food
                </button>
            `;


            container.appendChild(
                card
            );
        }
    );
}


/* =========================================================
   SELECT FOOD FOR REQUEST
   ========================================================= */

async function requestAvailableFood(
    donationId
) {

    try {

        const result =
            await apiRequest(
                "/donations/" +
                donationId,
                {
                    method: "GET"
                }
            );


        if (!result) {
            return;
        }


        const donation =
            result.donation ||
            result.data ||
            result;


        const foodInput =
            document.getElementById(
                "requiredFood"
            );


        if (foodInput) {

            foodInput.value =
                donation.food_name ||
                "";

            const section =
                document.getElementById(
                    "request-food"
                );

            if (section) {

                section.scrollIntoView({
                    behavior: "smooth"
                });
            }


            const message =
                document.getElementById(
                    "requestMessage"
                );

            if (message) {

                message.textContent =
                    "✅ Food selected: " +
                    (
                        donation.food_name ||
                        ""
                    );

                message.style.color =
                    "#2e7d32";
            }
        }


    } catch (error) {

        console.error(
            "Food selection error:",
            error
        );

        alert(
            "Could not load food details."
        );
    }
}


/* =========================================================
   VOLUNTEER PROFILE
   ========================================================= */

const volunteerProfileForm =
    document.getElementById(
        "volunteerProfileForm"
    );


if (volunteerProfileForm) {

    volunteerProfileForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            if (!requireLogin()) {
                return;
            }


            const vehicleElement =
                document.getElementById(
                    "vehicleType"
                );

            const phoneElement =
                document.getElementById(
                    "volunteerPhone"
                );

            const cityElement =
                document.getElementById(
                    "volunteerCity"
                );


            try {

                const result =
                    await apiRequest(
                        "/volunteer/profile",
                        {
                            method: "POST",

                            body: JSON.stringify({
                                vehicle_type:
                                    vehicleElement
                                        ? vehicleElement.value
                                        : "",

                                phone:
                                    phoneElement
                                        ? phoneElement.value
                                        : "",

                                city:
                                    cityElement
                                        ? cityElement.value
                                        : ""
                            })
                        }
                    );


                if (!result) {
                    return;
                }


                if (
                    !result.ok &&
                    !result.success
                ) {

                    alert(
                        "❌ " +
                        (
                            result.error ||
                            result.message ||
                            result.detail ||
                            "Profile update failed."
                        )
                    );

                    return;
                }


                alert(
                    "✅ Volunteer profile saved successfully!"
                );


            } catch (error) {

                console.error(
                    "Volunteer profile error:",
                    error
                );

                alert(
                    "❌ Could not connect to backend."
                );
            }
        }
    );
}


/* =========================================================
   VOLUNTEER AVAILABLE DELIVERIES
   ========================================================= */

async function loadAvailableDeliveries() {

    if (!requireLogin()) {
        return;
    }


    try {

        const result =
            await apiRequest(
                "/volunteer/available-deliveries",
                {
                    method: "GET"
                }
            );


        if (!result) {
            return;
        }


        const deliveries =
            Array.isArray(result)
                ? result
                : (
                    result.deliveries ||
                    result.data ||
                    []
                );


        displayAvailableDeliveries(
            deliveries
        );


    } catch (error) {

        console.error(
            "Available deliveries error:",
            error
        );
    }
}


/* =========================================================
   DISPLAY AVAILABLE DELIVERIES
   ========================================================= */

function displayAvailableDeliveries(
    deliveries
) {

    const container =
        document.getElementById(
            "availableDeliveryList"
        );


    if (!container) {
        return;
    }


    container.innerHTML = "";


    if (
        !Array.isArray(deliveries) ||
        deliveries.length === 0
    ) {

        container.innerHTML = `
            <p style="text-align:center;">
                No deliveries available.
            </p>
        `;

        return;
    }


    deliveries.forEach(
        function (delivery) {

            const item =
                document.createElement(
                    "div"
                );


            item.className =
                "delivery-card";


            item.innerHTML = `
                <h3>
                    🚚 Delivery #${escapeHTML(
                        delivery.id
                    )}
                </h3>

                <p>
                    📦 Donation:
                    ${escapeHTML(
                        delivery.donation_id
                    )}
                </p>

                <p>
                    📍 Pickup:
                    ${escapeHTML(
                        delivery.pickup_location ||
                        "-"
                    )}
                </p>

                <p>
                    🏠 Delivery:
                    ${escapeHTML(
                        delivery.delivery_location ||
                        "-"
                    )}
                </p>

                <p>
                    Status:
                    ${escapeHTML(
                        delivery.status ||
                        "PENDING"
                    )}
                </p>

                <button
                    onclick="acceptDelivery(${delivery.id})">
                    Accept Delivery
                </button>
            `;


            container.appendChild(
                item
            );
        }
    );
}


/* =========================================================
   VOLUNTEER MY DELIVERIES
   ========================================================= */

async function loadMyDeliveries() {

    if (!requireLogin()) {
        return;
    }


    try {

        const result =
            await apiRequest(
                "/volunteer/my-deliveries",
                {
                    method: "GET"
                }
            );


        if (!result) {
            return;
        }


        const deliveries =
            Array.isArray(result)
                ? result
                : (
                    result.deliveries ||
                    result.data ||
                    []
                );


        displayMyDeliveries(
            deliveries
        );


    } catch (error) {

        console.error(
            "My deliveries error:",
            error
        );
    }
}


/* =========================================================
   DISPLAY MY DELIVERIES
   ========================================================= */

function displayMyDeliveries(
    deliveries
) {

    const container =
        document.getElementById(
            "myDeliveryList"
        );


    if (!container) {
        return;
    }


    container.innerHTML = "";


    if (
        !Array.isArray(deliveries) ||
        deliveries.length === 0
    ) {

        container.innerHTML = `
            <p style="text-align:center;">
                You have no deliveries yet.
            </p>
        `;

        return;
    }


    deliveries.forEach(
        function (delivery) {

            const item =
                document.createElement(
                    "div"
                );


            item.className =
                "delivery-card";


            item.innerHTML = `
                <h3>
                    🚚 Delivery #${escapeHTML(
                        delivery.id
                    )}
                </h3>

                <p>
                    📦 Donation:
                    ${escapeHTML(
                        delivery.donation_id
                    )}
                </p>

                <p>
                    📍 Pickup:
                    ${escapeHTML(
                        delivery.pickup_location ||
                        "-"
                    )}
                </p>

                <p>
                    🏠 Delivery:
                    ${escapeHTML(
                        delivery.delivery_location ||
                        "-"
                    )}
                </p>

                <p>
                    Status:
                    <strong>
                        ${escapeHTML(
                            delivery.status ||
                            "-"
                        )}
                    </strong>
                </p>

                <div class="delivery-actions">

                    <button
                        onclick="pickupDelivery(${delivery.id})">
                        Pickup
                    </button>

                    <button
                        onclick="startDelivery(${delivery.id})">
                        Start
                    </button>

                    <button
                        onclick="completeDelivery(${delivery.id})">
                        Complete
                    </button>

                </div>
            `;


            container.appendChild(
                item
            );
        }
    );
}


/* =========================================================
   ACCEPT DELIVERY
   ========================================================= */

async function acceptDelivery(
    deliveryId
) {

    if (!requireLogin()) {
        return;
    }


    try {

        const result =
            await apiRequest(
                "/volunteer/delivery/" +
                deliveryId +
                "/accept",
                {
                    method: "POST",
                    body: JSON.stringify({})
                }
            );


        if (!result) {
            return;
        }


        if (
            !result.ok &&
            !result.success
        ) {

            alert(
                "❌ " +
                (
                    result.error ||
                    result.message ||
                    result.detail ||
                    "Could not accept delivery."
                )
            );

            return;
        }


        alert(
            "✅ Delivery accepted!"
        );


        loadAvailableDeliveries();

        loadMyDeliveries();


    } catch (error) {

        console.error(
            "Accept delivery error:",
            error
        );

        alert(
            "❌ Could not connect to backend."
        );
    }
}


/* =========================================================
   PICKUP DELIVERY
   ========================================================= */

async function pickupDelivery(
    deliveryId
) {

    if (!requireLogin()) {
        return;
    }


    try {

        const result =
            await apiRequest(
                "/volunteer/delivery/" +
                deliveryId +
                "/pickup",
                {
                    method: "POST",
                    body: JSON.stringify({})
                }
            );


        if (!result) {
            return;
        }


        if (
            !result.ok &&
            !result.success
        ) {

            alert(
                "❌ " +
                (
                    result.error ||
                    result.message ||
                    result.detail ||
                    "Pickup update failed."
                )
            );

            return;
        }


        alert(
            "✅ Food marked as picked up!"
        );


        loadMyDeliveries();


    } catch (error) {

        console.error(
            "Pickup error:",
            error
        );

        alert(
            "❌ Could not connect to backend."
        );
    }
}


/* =========================================================
   START DELIVERY
   ========================================================= */

async function startDelivery(
    deliveryId
) {

    if (!requireLogin()) {
        return;
    }


    try {

        const result =
            await apiRequest(
                "/volunteer/delivery/" +
                deliveryId +
                "/start",
                {
                    method: "POST",
                    body: JSON.stringify({})
                }
            );


        if (!result) {
            return;
        }


        if (
            !result.ok &&
            !result.success
        ) {

            alert(
                "❌ " +
                (
                    result.error ||
                    result.message ||
                    result.detail ||
                    "Could not start delivery."
                )
            );

            return;
        }


        alert(
            "🚚 Delivery started!"
        );


        loadMyDeliveries();


    } catch (error) {

        console.error(
            "Start delivery error:",
            error
        );

        alert(
            "❌ Could not connect to backend."
        );
    }
}


/* =========================================================
   COMPLETE DELIVERY
   ========================================================= */

async function completeDelivery(
    deliveryId
) {

    if (!requireLogin()) {
        return;
    }


    try {

        const result =
            await apiRequest(
                "/volunteer/delivery/" +
                deliveryId +
                "/complete",
                {
                    method: "POST",
                    body: JSON.stringify({})
                }
            );


        if (!result) {
            return;
        }


        if (
            !result.ok &&
            !result.success
        ) {

            alert(
                "❌ " +
                (
                    result.error ||
                    result.message ||
                    result.detail ||
                    "Could not complete delivery."
                )
            );

            return;
        }


        alert(
            "✅ Delivery completed successfully!"
        );


        loadMyDeliveries();


    } catch (error) {

        console.error(
            "Complete delivery error:",
            error
        );

        alert(
            "❌ Could not connect to backend."
        );
    }
}


/* =========================================================
   VOLUNTEER PROFILE LOAD
   ========================================================= */

async function loadVolunteerProfile() {

    if (!requireLogin()) {
        return;
    }


    try {

        const result =
            await apiRequest(
                "/volunteer/profile",
                {
                    method: "GET"
                }
            );


        if (!result) {
            return;
        }


        const profile =
            result.profile ||
            result.data ||
            result;


        const vehicleElement =
            document.getElementById(
                "vehicleType"
            );

        const phoneElement =
            document.getElementById(
                "volunteerPhone"
            );

        const cityElement =
            document.getElementById(
                "volunteerCity"
            );


        if (
            vehicleElement &&
            profile.vehicle_type
        ) {

            vehicleElement.value =
                profile.vehicle_type;
        }


        if (
            phoneElement &&
            profile.phone
        ) {

            phoneElement.value =
                profile.phone;
        }


        if (
            cityElement &&
            profile.city
        ) {

            cityElement.value =
                profile.city;
        }


    } catch (error) {

        console.error(
            "Volunteer profile load error:",
            error
        );
    }
}


/* =========================================================
   NOTIFICATIONS
   ========================================================= */

async function loadNotifications() {

    if (!requireLogin()) {
        return;
    }


    try {

        const result =
            await apiRequest(
                "/notifications",
                {
                    method: "GET"
                }
            );


        if (!result) {
            return;
        }


        const notifications =
            Array.isArray(result)
                ? result
                : (
                    result.notifications ||
                    result.data ||
                    []
                );


        displayNotifications(
            notifications
        );


    } catch (error) {

        console.error(
            "Notification error:",
            error
        );
    }
}


/* =========================================================
   DISPLAY NOTIFICATIONS
   ========================================================= */

function displayNotifications(
    notifications
) {

    const container =
        document.getElementById(
            "notificationList"
        );


    if (!container) {
        return;
    }


    container.innerHTML = "";


    if (
        !Array.isArray(notifications) ||
        notifications.length === 0
    ) {

        container.innerHTML = `
            <p>
                No notifications.
            </p>
        `;

        return;
    }


    notifications.forEach(
        function (notification) {

            const item =
                document.createElement(
                    "div"
                );


            item.className =
                notification.is_read
                    ? "notification read"
                    : "notification unread";


            item.innerHTML = `
                <p>
                    ${escapeHTML(
                        notification.message
                    )}
                </p>

                <small>
                    ${formatDate(
                        notification.created_at
                    )}
                </small>

                ${
                    notification.is_read
                        ? ""
                        : `
                            <button
                                onclick="markNotificationRead(${notification.id})">
                                Mark as read
                            </button>
                        `
                }
            `;


            container.appendChild(
                item
            );
        }
    );
}


/* =========================================================
   MARK NOTIFICATION READ
   ========================================================= */

async function markNotificationRead(
    notificationId
) {

    if (!requireLogin()) {
        return;
    }


    try {

        const result =
            await apiRequest(
                "/notifications/" +
                notificationId +
                "/read",
                {
                    method: "PUT",
                    body: JSON.stringify({})
                }
            );


        if (!result) {
            return;
        }


        loadNotifications();


    } catch (error) {

        console.error(
            "Notification read error:",
            error
        );
    }
}


/* =========================================================
   DONOR ANALYTICS
   ========================================================= */

async function loadDonorAnalytics() {

    if (!requireLogin()) {
        return;
    }


    try {

        const result =
            await apiRequest(
                "/analytics/donor",
                {
                    method: "GET"
                }
            );


        if (!result) {
            return;
        }


        console.log(
            "Donor analytics:",
            result
        );


    } catch (error) {

        console.error(
            "Donor analytics error:",
            error
        );
    }
}


/* =========================================================
   NGO ANALYTICS
   ========================================================= */

async function loadNGOAnalytics() {

    if (!requireLogin()) {
        return;
    }


    try {

        const result =
            await apiRequest(
                "/analytics/ngo",
                {
                    method: "GET"
                }
            );


        if (!result) {
            return;
        }


        console.log(
            "NGO analytics:",
            result
        );


    } catch (error) {

        console.error(
            "NGO analytics error:",
            error
        );
    }
}


/* =========================================================
   ADMIN ANALYTICS
   ========================================================= */

async function loadAdminAnalytics() {

    if (!requireLogin()) {
        return;
    }


    try {

        const result =
            await apiRequest(
                "/analytics/admin",
                {
                    method: "GET"
                }
            );


        if (!result) {
            return;
        }


        console.log(
            "Admin analytics:",
            result
        );


    } catch (error) {

        console.error(
            "Admin analytics error:",
            error
        );
    }
}


/* =========================================================
   ADMIN USERS
   ========================================================= */

async function loadAdminUsers() {

    if (!requireLogin()) {
        return;
    }


    try {

        const result =
            await apiRequest(
                "/admin/users",
                {
                    method: "GET"
                }
            );


        if (!result) {
            return;
        }


        console.log(
            "Admin users:",
            result
        );


    } catch (error) {

        console.error(
            "Admin users error:",
            error
        );
    }
}


/* =========================================================
   ADMIN NGOS
   ========================================================= */

async function loadAdminNGOs() {

    if (!requireLogin()) {
        return;
    }


    try {

        const result =
            await apiRequest(
                "/admin/ngos",
                {
                    method: "GET"
                }
            );


        if (!result) {
            return;
        }


        console.log(
            "Admin NGOs:",
            result
        );


    } catch (error) {

        console.error(
            "Admin NGO error:",
            error
        );
    }
}


/* =========================================================
   ADMIN DONATIONS
   ========================================================= */

async function loadAdminDonations() {

    if (!requireLogin()) {
        return;
    }


    try {

        const result =
            await apiRequest(
                "/admin/donations",
                {
                    method: "GET"
                }
            );


        if (!result) {
            return;
        }


        console.log(
            "Admin donations:",
            result
        );


    } catch (error) {

        console.error(
            "Admin donations error:",
            error
        );
    }
}


/* =========================================================
   ADMIN DELIVERIES
   ========================================================= */

async function loadAdminDeliveries() {

    if (!requireLogin()) {
        return;
    }


    try {

        const result =
            await apiRequest(
                "/admin/deliveries",
                {
                    method: "GET"
                }
            );


        if (!result) {
            return;
        }


        console.log(
            "Admin deliveries:",
            result
        );


    } catch (error) {

        console.error(
            "Admin deliveries error:",
            error
        );
    }
}


/* =========================================================
   ADMIN STATISTICS
   ========================================================= */

async function loadAdminStats() {

    if (!requireLogin()) {
        return;
    }


    try {

        const result =
            await apiRequest(
                "/admin/stats",
                {
                    method: "GET"
                }
            );


        if (!result) {
            return;
        }


        console.log(
            "Admin stats:",
            result
        );


    } catch (error) {

        console.error(
            "Admin stats error:",
            error
        );
    }
}


/* =========================================================
   NGO PROFILE
   ========================================================= */

async function loadNGOProfile() {

    if (!requireLogin()) {
        return;
    }


    try {

        const result =
            await apiRequest(
                "/ngo/profile",
                {
                    method: "GET"
                }
            );


        if (!result) {
            return;
        }


        console.log(
            "NGO profile:",
            result
        );


    } catch (error) {

        console.error(
            "NGO profile error:",
            error
        );
    }
}


/* =========================================================
   NGO PAGE SEARCH
   ========================================================= */

function filterAvailableFood() {

    const searchInput =
        document.getElementById(
            "foodSearch"
        );

    const typeFilter =
        document.getElementById(
            "foodTypeFilter"
        );

    const rows =
        document.querySelectorAll(
            "#availableFoodList tr"
        );


    if (!searchInput) {
        return;
    }


    const search =
        searchInput.value
            .toLowerCase()
            .trim();


    const type =
        typeFilter
            ? typeFilter.value
                .toLowerCase()
                .trim()
            : "";


    rows.forEach(
        function (row) {

            const text =
                row.textContent
                    .toLowerCase();


            const matchesSearch =
                text.includes(search);


            const matchesType =
                !type ||
                text.includes(type);


            row.style.display =
                matchesSearch &&
                matchesType
                    ? ""
                    : "none";
        }
    );
}


/* =========================================================
   NEED FOOD SEARCH
   ========================================================= */

function filterNeedFood() {

    const searchElement =
        document.getElementById(
            "needFoodSearch"
        );

    const typeElement =
        document.getElementById(
            "needFoodType"
        );

    const cards =
        document.querySelectorAll(
            "#needFoodList .available-food-card"
        );


    if (!searchElement) {
        return;
    }


    const search =
        searchElement.value
            .toLowerCase()
            .trim();


    const type =
        typeElement
            ? typeElement.value
                .toLowerCase()
                .trim()
            : "";


    cards.forEach(
        function (card) {

            const text =
                card.textContent
                    .toLowerCase();


            const matchesSearch =
                text.includes(search);


            const matchesType =
                !type ||
                text.includes(type);


            card.style.display =
                matchesSearch &&
                matchesType
                    ? ""
                    : "none";
        }
    );
}


/* =========================================================
   PAGE INITIALIZATION
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const page =
            window.location.pathname
                .split("/")
                .pop()
                .toLowerCase();


        /* -------------------------
           LOGIN PAGE
           ------------------------- */

        if (
            page === "login.html"
        ) {

            /*
             * Do NOT automatically show
             * session expired here.
             *
             * User can simply login again.
             */

            return;
        }


        /* -------------------------
           REGISTER PAGE
           ------------------------- */

        if (
            page === "register.html"
        ) {

            return;
        }


        /* -------------------------
           DONOR DASHBOARD
           ------------------------- */

        if (
            page === "dashboard.html"
        ) {

            loadDonorDashboard();

            loadNotifications();

            return;
        }


        /* -------------------------
           DONATE PAGE
           ------------------------- */

        if (
            page === "donate.html"
        ) {

            requireLogin();

            return;
        }


        /* -------------------------
           NGO DASHBOARD
           ------------------------- */

        if (
            page === "ngo_dashboard.html" ||
            page === "ngo-dashboard.html"
        ) {

            loadNGOAvailableFood();

            loadNGOClaims();

            loadNGOFoodRequests();

            loadNGOProfile();

            loadNotifications();

            return;
        }


        /* -------------------------
           NEED FOOD
           ------------------------- */

        if (
            page === "need_food.html" ||
            page === "need-food.html"
        ) {

            loadNeedFood();

            return;
        }


        /* -------------------------
           VOLUNTEER
           ------------------------- */

        if (
            page === "volunteer.html"
        ) {

            loadVolunteerProfile();

            loadAvailableDeliveries();

            loadMyDeliveries();

            loadNotifications();

            return;
        }


        /* -------------------------
           ADMIN
           ------------------------- */

        if (
            page === "admin.html"
        ) {

            loadAdminUsers();

            loadAdminNGOs();

            loadAdminDonations();

            loadAdminDeliveries();

            loadAdminStats();

            loadAdminAnalytics();

            loadNotifications();

            return;
        }

    }
);


/* =========================================================
   BACKWARD COMPATIBILITY FUNCTIONS
   =========================================================

   These prevent older HTML onclick handlers
   from causing "function not defined" errors.
   ========================================================= */

function displayDonations() {
    loadDonorDashboard();
}


function displayAvailableFood() {
    loadNGOAvailableFood();
}


function displayNGORequests() {
    loadNGOClaims();
}


function displayPickups() {
    loadNGOClaims();
}


function updateDonorStatistics() {
    loadDonorDashboard();
}


function updateNGOStatistics() {
    loadNGOClaims();
}


function displayNeedFood() {
    loadNeedFood();
}


/* =========================================================
   END OF SCRIPT
   ========================================================= */