document.addEventListener("DOMContentLoaded", function () {

    function getCookie(name) {
        if (!document.cookie) {
            return null;
        }

        const xsrfCookies = document.cookie.split(';')
            .map(c => c.trim())
            .filter(c => c.startsWith(name + '='));

        if (xsrfCookies.length === 0) {
            return null;
        }
        return decodeURIComponent(xsrfCookies[0].split('=')[1]);
    }

    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.querySelectorAll("li")].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
            const triggerButton = document.querySelector(".help--slides-pagination").querySelector("a");
            triggerButton.click();
        }

        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;
            // stara wersja, raczej błędna
            // const pageButtons = document.querySelector(".help--slides-pagination");
            const pageButtons = e.target.parentElement.parentElement.parentElement.querySelector(".help--slides-pagination");
            const listElements = document.querySelector(".help--slides.active").querySelector("ul").querySelectorAll("li");

            [...pageButtons.children].forEach(function (li) {
                li.firstChild.classList.remove("active");

                if (li.firstChild.dataset.page === page) {
                    li.firstChild.classList.add("active");
                }

                listElements.forEach((el) => {
                    if (el.dataset.page === page) {
                        el.style.display = "flex";
                    } else {
                        el.style.display = "none";
                    }
                })
            });
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    if (window.location.pathname === '/') {
        const triggerButton = document.querySelector(".help--slides-pagination").querySelector("a");
        triggerButton.click();
    }


    /**
     * Only for / endpoint (Warning: hardcoded)
     * Fetching bags and institutions
     * numbers in real time
     */

    const totalBags = document.querySelector(".total_bags");
    const totalInstitutions = document.querySelector(".total_institutions");

    if (window.location.pathname === '/') {
        let url = window.location.origin + window.location.pathname;
        let urlHome = (url + "?fetch_stats=1").toString();
        const intervalHome = setInterval(function () {
            fetch(urlHome)
                .then((response) => {
                    return response.json();
                })
                .then((data) => {
                    totalBags.textContent = data["total_bags"];
                    totalInstitutions.textContent = data["total_institutions"];
                })
        }, 5000);
    }

    /**
     * Only for /add_donation/ endpoint (Warning: hardcoded)
     * Working with 5 steps of form input
     */

    function bagsValidator(num) {
        return !isNaN(parseFloat(num)) && isFinite(num) && Math.floor(num) == num && num > 0;
    }

    if (window.location.pathname === '/add-donation/') {
        // collecting div with error messages for later use
        const errorMsg = document.querySelector(".error-message")

        function manageError(command, messages = []) {
            if (command === "show") {
                errorMsg.innerHTML = '';
                messages.forEach(message => {
                    errorMsg.innerHTML += `<span>${message}</span>`;
                });
                errorMsg.style.display = "block";
            } else {
                errorMsg.style.display = "none";
            }
        }


        // transition STEP 1 - STEP 2
        const buttonStep1 = document.querySelector(".step1");
        let chosenCategoriesNames;
        let chosenCategoriesIds;
        buttonStep1.addEventListener("click", (e) => {

            // getting list of chosen categories
            chosenCategoriesNames = [];
            chosenCategoriesIds = [];
            const inputs = e.target.parentElement.parentElement.querySelectorAll("input");
            inputs.forEach(input => {
                if (input.checked) {
                    chosenCategoriesNames.push(input.id);
                    chosenCategoriesIds.push(input.value);
                }
            });

            // validation before going to STEP 2
            if (chosenCategoriesNames.length === 0) {
                e.stopImmediatePropagation();
                manageError("show", ["Wybierz przynajmniej jedną kategorię"]);
            } else {
                manageError("hide");
            }
        });


        // Transition STEP 2 - STEP 3
        const buttonStep2 = document.querySelector(".step2");
        let bags = 0;

        buttonStep2.addEventListener("click", (e) => {

            // collecting and validating number of bags input from STEP 2
            const bagsInput = e.target.parentElement.parentElement.querySelector("input");

            // if input in STEP 2 is correct bags will take its value, proceed to STEP 3
            if (bagsInput.value && bagsValidator(bagsInput.value)) {
                bags = Number(bagsInput.value);
                manageError("hide");
                // Listing institutions in STEP 3 that matches the criteria from STEP 1
                const institutionsContainer = document.querySelector(".data-step-3");
                displayInstitutions(institutionsContainer, chosenCategoriesNames);
            } else {
                e.stopImmediatePropagation();
                manageError("show", ["Podaj poprawną liczbę worków"]);
            }

            function displayInstitutions(institutionsContainer, chosenCategories) {
                const institutionsContainerAll = institutionsContainer.querySelector(".all-categories");
                const institutionsAll = institutionsContainerAll.querySelectorAll(".form-group--checkbox");
                const institutionsContainerSome = institutionsContainer.querySelector(".some-categories");
                const institutionsSome = institutionsContainerSome.querySelectorAll(".form-group--checkbox");
                let institutionsDuplicates = [];


                institutionsAll.forEach(institution => {
                    const institutionCategories = institution.querySelector(".categories").dataset.cat;
                    // All categories match
                    if (chosenCategories.every(cat => institutionCategories.includes(cat))) {
                        institution.style.display = "flex";
                        institutionsDuplicates.push(institution.querySelector(".title").textContent);
                    } else {
                        institution.style.display = "none";
                    }
                });

                // if only 1 category was selected, all- and some- lists are the same, so second one is not displayed
                let h4Element = institutionsContainerSome.previousSibling.previousSibling;
                if (chosenCategories.length <= 1) {
                    institutionsContainerSome.style.display = "none";
                    h4Element.style.display = "none";
                } else {
                    institutionsContainerSome.style.display = "block";
                    h4Element.style.display = "flex";

                    institutionsSome.forEach(institution => {
                        const institutionCategories = institution.querySelector(".categories").dataset.cat;
                        // Some categories match
                        if (chosenCategories.some(cat => institutionCategories.includes(cat))
                            && !institutionsDuplicates.includes(institution.querySelector(".title").textContent)) {
                            institution.style.display = "flex";
                        } else {
                            institution.style.display = "none";
                        }
                    });
                }

                displayEmptyContainer(institutionsContainerAll);
                // displayEmptyContainer(institutionsContainerSome);
            }

            function displayEmptyContainer(container) {
                let infoTag = container.querySelector("h4.error-message");
                let displayedData = [];

                [...container.children].forEach(child => {
                    if (child.style.display !== 'none' && child.tagName === 'DIV') {
                        displayedData.push(child);
                    }
                });
                if (displayedData.length === 0) {
                    infoTag.style.display = "flex"
                } else {
                    infoTag.style.display = "none";
                }
            }
        });


        // transition STEP 3 - STEP 4
        const buttonStep3 = document.querySelector(".step3");
        let chosenInstitutionName = [];
        let chosenInstitutionId;
        buttonStep3.addEventListener("click", e => {

            // collecting chosen institution from STEP 3
            const institutionsContainer = document.querySelector(".data-step-3");
            [...institutionsContainer.querySelectorAll(".form-group--checkbox")].forEach(box => {
                let input = box.querySelector("input");
                if (input && input.checked) {
                    chosenInstitutionName[0] = box.querySelector(".title").textContent;
                    chosenInstitutionName[1] = box.querySelector(".inst-type").dataset.type;
                    chosenInstitutionId = box.querySelector(".inst-type").dataset.pk;
                }
            });


            // validating selection
            if (chosenInstitutionName.length !== 2) {
                manageError("show", ["Wybierz dokładnie jedną organizację"]);
                e.stopImmediatePropagation();
            } else {
                manageError("hide");
            }
        });


        // transition STEP 4 - STEP 5
        const buttonStep4 = document.querySelector(".step4");
        buttonStep4.addEventListener("click", e => {

            // collecting all the info from STEP 4
            const formContainer = document.querySelector(".data-step-4");
            const addressInput = formContainer.querySelector("[name='address']");
            const cityInput = formContainer.querySelector("[name='city']");
            const postcodeInput = formContainer.querySelector("[name='zip_code']");
            const phoneInput = formContainer.querySelector("[name='phone_number']");
            const dateInput = formContainer.querySelector("[name='pick_up_date']");
            const timeInput = formContainer.querySelector("[name='pick_up_time']");
            const infoInput = formContainer.querySelector("[name='pick_up_comment']");
            const countryInput = formContainer.querySelector("[name='country']");

            // validators for the input
            function validateAddress(data) {
                return data.length >= 3;
            }

            function validateCity(data) {
                return data.length >= 3;
            }

            function isDigit(data) {
                return [...data].every(char => ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"].includes(char))
            }

            function extract(data, symbols = []) {
                let result = [];
                [...data].forEach(char => {
                    if (isDigit(char) || symbols.includes(char)) {
                        result.push(char);
                    }
                });
                return result.join("");
            }

            function validateZipCode(data) {
                let cleanedCode = extract(data, ["-"])
                if (cleanedCode.includes("-")) {
                    let cleanedCodeArray = cleanedCode.split("-");
                    if (extract(cleanedCodeArray[0]).length === 2 && extract(cleanedCodeArray[1]).length === 3) {
                        return true;
                    }
                } else {
                    return extract(cleanedCode).length === 5;
                }
            }

            const polishPrefixes = ["12", "13", "14", "15", "16", "17", "18", "22", "23", "24", "25", "29", "32", "33", "34",
                "41", "42", "43", "44", "46", "48", "52", "54", "55", "56", "58", "59", "61", "62", "63",
                "65", "67", "68", "71", "74", "75", "76", "77", "81", "82", "83", "84", "85", "86", "87",
                "89", "91", "94", "95"] + ["50", "51", "53", "57", "60", "66", "69", "72", "73",
                "78", "79", "88"]

            function validatePhoneNumber(data) {
                let cleanedPhone = extract(data);
                return cleanedPhone.length === 9 && polishPrefixes.includes(cleanedPhone.slice(0, 2))
            }

            function getTomorrow() {
                let today = new Date();
                let tomorrow = new Date(today);
                tomorrow.setHours(0);
                tomorrow.setMinutes(0);
                tomorrow.setSeconds(0);
                tomorrow.setDate(tomorrow.getDate() + 1);
                return tomorrow;
            }

            function validateDate(date_data) {
                let inputDate = new Date(date_data);
                return inputDate >= getTomorrow();
            }

            function validateTime(time_data) {
                let timeInput = time_data.split(":");
                let hour = Number(timeInput[0]);
                let minute = Number(timeInput[1]);
                return hour >= 9 && (hour < 20 || (hour === 20 && minute === 0));
            }

            let countriesArray = [
                {"country": "Polska", "number": "+48"},
                {"country": "Niemcy", "number": "+49"},
                {"country": "Ukraina", "number": "+380"},
            ];
            let countriesNumbers = countriesArray.map(item => item.number);

            function validateCountry(data) {
                return countriesNumbers.includes(data);
            }

            // input validation before going to STEP 5
            let errors = [];
            if (!addressInput.value) {
                errors.push("Wpisz poprawny adres");
            } else if (!validateAddress(addressInput.value)) {
                errors.push("Wpisz poprawny adres");
            }
            if (!cityInput.value) {
                errors.push("Wpisz poprawne miasto");
            } else if (!validateCity(cityInput.value)) {
                errors.push("Wpisz poprawne miasto");
            }
            if (!postcodeInput.value) {
                errors.push("Wpisz poprawny kod pocztowy");
            } else if (!validateZipCode(postcodeInput.value)) {
                errors.push("Wpisz poprawny kod pocztowy");
            }
            if (!countryInput.value) {
                errors.push("Wybierz kraj");
            } else if (!validateCountry(countryInput.value)) {
                errors.push("Wybierz kraj");
            }
            if (!phoneInput.value) {
                errors.push("Wpisz poprawny numer telefonu");
            } else if (!validatePhoneNumber(phoneInput.value)) {
                errors.push("Wpisz poprawny numer telefonu");
            }
            if (!dateInput.value) {
                errors.push("Wpisz poprawną datę (najwcześniej jutro)");
            } else if (!validateDate(dateInput.value)) {
                errors.push("Wpisz poprawną datę (najwcześniej jutro)");
            }
            if (!timeInput.value) {
                errors.push("Wpisz poprawny czas (9-20)");
            } else if (!validateTime(timeInput.value)) {
                errors.push("Wpisz poprawny czas (9-20)");
            }

            // display message only when input is wrong
            if (errors.length) {
                e.stopImmediatePropagation();
                manageError("show", errors);
            } else {
                manageError("hide");
                lastTransition();
            }

            // setting variable to count errors in summary
            let errorCount = 0;

            function lastTransition() {
                // displaying data from previous inputs in STEP 5
                const summaryContainer = document.querySelector(".data-step-5");

                // letting user know if there are any mistakes
                const whatAndHowMany = summaryContainer.querySelector(".what-and-how-many");
                if (chosenCategoriesNames.length === 0) {
                    whatAndHowMany.textContent = "Wróć do kroku 1 i wybierz poprawną kategorię darów (przynajmniej 1)";
                    errorCount++;
                } else if (!bagsValidator(bags)) {
                    whatAndHowMany.textContent = "Wróć do kroku 2 i wpisz poprawną liczbę worków (więcej niż 0)";
                    errorCount++;
                } else {
                    whatAndHowMany.textContent = `Liczba worków: ${bags}, dary: ${chosenCategoriesNames.join(", ")}`;
                }

                let names = ["Inna organizacja", "Fundacja", "Organizacja pozarządowa", "Lokalna zbiórka"];

                const toWho = summaryContainer.querySelector(".to-who");
                if (!chosenInstitutionName) {
                    toWho.textContent = "Wróć do kroku 3 i wybierz poprawną instytucję (1)";
                    errorCount++;
                } else {
                    toWho.textContent = `Obdarowana: ${names[chosenInstitutionName[1]]} ${chosenInstitutionName[0]}`;
                }

                const address = summaryContainer.querySelector(".address");
                if (!validateAddress(addressInput.value)) {
                    address.textContent = "Wróć do kroku 4 i wpisz poprawny adres";
                    errorCount++;
                } else {
                    address.textContent = addressInput.value;
                }

                const city = summaryContainer.querySelector(".city");
                if (!validateCity(cityInput.value)) {
                    city.textContent = "Wróć do kroku 4 i wpisz poprawne miasto";
                    errorCount++;
                } else {
                    city.textContent = cityInput.value;
                }

                const postcode = summaryContainer.querySelector(".postcode");
                if (!validateZipCode(postcodeInput.value)) {
                    postcode.textContent = "Wróć do kroku 4 i wpisz poprawny kod pocztowy";
                    errorCount++;
                } else {
                    postcode.textContent = extract(postcodeInput.value, ["-"]);
                }

                const phone = summaryContainer.querySelector(".phone");
                if (!validatePhoneNumber(phoneInput.value) || !validateCountry(countryInput.value)) {
                    phone.textContent = "Wróć do kroku 4 i wpisz poprawny numer telefonu oraz kraj";
                    errorCount++;
                } else {
                    phone.textContent = countryInput.value + extract(phoneInput.value);
                }

                const date = summaryContainer.querySelector(".date");
                if (!validateDate(dateInput.value)) {
                    date.textContent = "Wróć do kroku 4 i wpisz poprawną datę (najwcześniej jutro)";
                    errorCount++;
                } else {
                    date.textContent = dateInput.value;
                }

                const time = summaryContainer.querySelector(".time");
                if (!validateTime(timeInput.value)) {
                    time.textContent = "Wróć do kroku 4 i wpisz poprawny czas (9-20)";
                    errorCount++;
                } else {
                    time.textContent = timeInput.value;
                }

                const info = summaryContainer.querySelector(".info");
                if (!infoInput.value) {
                    info.textContent = "Brak uwag";
                } else {
                    info.textContent = infoInput.value;
                }
            }

            // submitting the form
            const submitButton = document.querySelector("button[type='submit']");
            submitButton.addEventListener("click", e => {
                if (errorCount > 0) {
                    e.stopImmediatePropagation();
                } else {
                    e.preventDefault();
                    let url = window.location.href;
                    submitFetch(url);
                }
            });

            function submitFetch(url) {
                const csrfToken = getCookie('csrftoken');

                fetch(url, {
                    method: 'POST',
                    body: JSON.stringify({
                        bags: bags,
                        categories: chosenCategoriesIds,
                        institution: chosenInstitutionId,
                        address: addressInput.value,
                        phone_number: countryInput.value + extract(phoneInput.value),
                        city: cityInput.value,
                        zip_code: extract(postcodeInput.value, ["-"]),
                        pick_up_date: dateInput.value,
                        pick_up_time: timeInput.value,
                        pick_up_comment: infoInput.value,
                    }),
                    headers: {
                        'Content-type': 'application/json; charset=UTF-8',
                        'X-CSRFTOKEN': csrfToken,
                    }
                })
                    .then(response => {
                        window.location = response.url
                        // return response.json()
                    })
                    .then(data => {
                        // console.log(data)
                    }).catch(error => console.error('Error:', error));
            }
        });
    }


    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            // this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary
        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {
            e.preventDefault();
            this.currentStep++;
            this.updateForm();
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }

    /**
     * Only for accounts/profile/ endpoint (Warning: hardcoded)
     * Displaying users donations
     */
    if (window.location.pathname === "/accounts/profile/") {
        const donationsContainer = document.querySelector("#donation-container");
        const activeDonationsContainer = donationsContainer.querySelector(".active-donations");
        const inactiveDonationsContainer = donationsContainer.querySelector(".inactive-donations");
        activateButtons();

        function activateButtons() {
            const takenButtons = donationsContainer.querySelectorAll(".taken-button");
            takenButtons.forEach(button => {
                button.addEventListener("click", e => {
                    e.preventDefault();
                    let donationId = e.target.dataset.id;
                    let takenStatus = e.target.dataset.status;
                    fetchDonation(window.location.href, donationId, takenStatus);
                });
            });

        }


        function fetchDonation(url, pk, takenStatus) {
            fetch(url, {
                method: 'POST',
                body: JSON.stringify({
                    donationId: pk,
                    takenStatus: takenStatus,
                }),
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                    'X-CSRFTOKEN': getCookie('csrftoken'),
                }
            })
                .then(response => {
                    return response.json();
                })
                .then(data => {
                    // console.log(data.donation);
                    BobTheBuilder(data.donation);
                }).catch(error => console.error('Error:', error));
        }


        // removing particular row and creating new one below
        // function BobTheBuilder(donation) {
        //     [...activeDonationsContainer.children].forEach(child => {
        //         if (child.querySelector(".taken-button").dataset.id == donation.pk) {
        //             activeDonationsContainer.removeChild(child);
        //
        //             let h4 = document.createElement("h4");
        //             h4.classList.add("row", "m-3");
        //
        //             let institutionDiv = document.createElement("div");
        //             institutionDiv.classList.add("col-0", "col-md-3", "text-decoration-line-through");
        //             institutionDiv.textContent = donation.institution;
        //             h4.appendChild(institutionDiv);
        //
        //             let quantityDiv = document.createElement("div");
        //             quantityDiv.classList.add("col-0", "col-md-1", "text-center", "text-decoration-line-through");
        //             quantityDiv.textContent = donation.quantity;
        //             h4.appendChild(quantityDiv);
        //
        //             let dateDiv = document.createElement("div");
        //             dateDiv.classList.add("col-0", "col-md-3", "text-decoration-line-through");
        //             let dateArray = donation.pick_up_date.split("-");
        //             let date = `${dateArray[2]}/${dateArray[1]}/${dateArray[0]}`
        //             let timeArray = donation.pick_up_time.split(":");
        //             let time = `${timeArray[0]}:${timeArray[1]}`
        //             dateDiv.textContent = `${date} ${time}`;
        //             h4.appendChild(dateDiv);
        //
        //             let categoryDiv = document.createElement("div");
        //             categoryDiv.classList.add("col-0", "col-md-4", "text-decoration-line-through");
        //             categoryDiv.textContent = donation.categories.join(", ");
        //             h4.appendChild(categoryDiv);
        //
        //             let statusDiv = document.createElement("div");
        //             statusDiv.classList.add("col-0", "col-md-1", "text-center", "p-0");
        //             statusDiv.setAttribute("id", donation.pk);
        //             statusDiv.textContent = "Odebrane";
        //             h4.appendChild(statusDiv);
        //
        //             inactiveDonationsContainer.appendChild(h4);
        //         }
        //     });
        // }

        // Cloning whole node, possible backward fetch
        function BobTheBuilder(donation) {
            if (donation.status === 'true') {
                [...activeDonationsContainer.children].forEach(child => {
                    if (child.querySelector(".taken-button").dataset.id == donation.pk) {
                        let toClone = child.cloneNode(true);
                        let input = toClone.querySelector("input.btn");
                        input.value = "Przywróć";
                        input.dataset.status = "false";
                        let divs = [...toClone.querySelectorAll("div")];
                        divs.forEach(div => {
                            div.classList.add("text-decoration-line-through");
                        });

                        activeDonationsContainer.removeChild(child);
                        inactiveDonationsContainer.appendChild(toClone);
                        activateButtons();
                    }
                });
            } else {
                [...inactiveDonationsContainer.children].forEach(child => {
                    if (child.querySelector(".taken-button").dataset.id == donation.pk) {
                        let toClone = child.cloneNode(true);
                        let input = toClone.querySelector("input.btn");
                        input.value = "Zamknij";
                        input.dataset.status = "true";
                        let divs = [...toClone.querySelectorAll("div")];
                        divs.forEach(div => {
                            div.classList.remove("text-decoration-line-through");
                        });

                        inactiveDonationsContainer.removeChild(child);
                        activeDonationsContainer.appendChild(toClone);
                        activateButtons();
                    }
                });
            }
        }
    }

    /**
     * Only for accounts/settings/ endpoint (Warning: hardcoded)
     * Display form with user data
     */
    if (window.location.pathname === "/accounts/settings/") {
        const submitButton = document.querySelector(".btn[type='submit']");
        submitButton.addEventListener("click", submitListener)

        function submitListener(e) {
            e.preventDefault();
            const passInput1 = document.querySelector("#pass1").querySelector("input");
            const passInput2 = document.querySelector("#pass2").querySelector("input");
            const confMessage = document.querySelector(".confirmation-message");
            const spacer = document.querySelector(".spacer");

            // if password was not given yet
            if ([...passInput1.parentElement.classList].includes("d-none")) {
                spacer.remove();
                confMessage.classList.remove("d-none");
                passInput1.parentElement.classList.remove("d-none");
                submitButton.textContent = "Wyślij";
                // if password was already given
            } else if (passInput1.value) {
                passInput2.value = passInput1.value;
                submitButton.removeEventListener("click", submitListener);
                submitButton.click();
            }
        }
    }

    /**
     * Only for accounts/close/ endpoint (Warning: hardcoded)
     * Display form with user data
     */
    if (window.location.pathname === "/accounts/close/") {
        const submitButton = document.querySelector(".btn[type='submit']");
        const message = document.querySelector(".confirmation-message");
        const passInput1 = document.querySelector("#pass1").querySelector("input");
        const passInput2 = document.querySelector("#pass2").querySelector("input");

        submitButton.addEventListener("click", closeListener);

        function closeListener(e) {
            e.preventDefault();
            if (passInput1.value) {
                passInput2.value = passInput1.value;
                submitButton.removeEventListener("click", closeListener);
                submitButton.click();
            } else {
                message.style.background = "red";
            }
        }
    }

    /**
     * Only for accounts/password_reset/ endpoint (Warning: hardcoded)
     * Check if email exists in database
     */
    if (window.location.pathname === "/accounts/password_reset/") {
        const submitButton = document.querySelector(".btn[type='submit']");
        const message = document.querySelector(".confirmation-message");
        const emailInput = document.querySelector("#id_email");
        const redirect = document.querySelector("#email-redirect");
        const spacer = document.querySelector(".spacer");

        submitButton.addEventListener("click", emailListener);

        function emailListener(e) {
            e.preventDefault();
            if (emailInput.value) {
                fetchEmail(redirect.href, emailInput.value);
            }

            function fetchEmail(url, email) {
                fetch(url, {
                    method: 'POST',
                    body: JSON.stringify({
                        email: email,
                    }),
                    headers: {
                        'Content-type': 'application/json; charset=UTF-8',
                        'X-CSRFTOKEN': getCookie('csrftoken'),
                    }
                })
                    .then(response => {
                        return response.json();
                    })
                    .then(data => {
                        // console.log(data);
                        if (data.exists) {
                            submitButton.removeEventListener("click", emailListener);
                            submitButton.click();
                        } else {
                            spacer.remove();
                            message.classList.remove("d-none");
                            message.style.background = "red";
                        }
                    }).catch(error => console.error('Error:', error));
            }
        }
    }

    /**
     * Only for accounts/reset/.../set-password/ endpoint (Warning: hardcoded)
     * Checks if both password are similar
     */
    if (window.location.pathname.includes("set-password") || window.location.pathname.includes("password_change")) {
        const submitButton = document.querySelector(".btn[type='submit']");
        const message = document.querySelector(".confirmation-message");
        const spacer = document.querySelector(".spacer");
        const passInput1 = document.querySelector("#id_new_password1");
        const passInput2 = document.querySelector("#id_new_password2");

        submitButton.addEventListener("click", passwordListener);

        function passwordListener(e) {
            e.preventDefault();
            if (passInput1.value === passInput2.value) {
                submitButton.removeEventListener("click", passwordListener);
                submitButton.click();
            } else {
                spacer.remove();
                message.style.background = "red";
                message.classList.remove("d-none");
            }
        }
    }


});
