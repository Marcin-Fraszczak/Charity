document.addEventListener("DOMContentLoaded", function () {
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
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
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

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;
            const pageButtons = document.querySelector(".help--slides-pagination");
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
     * Only for / endpoint
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
     * Only for /add_donation/ endpoint
     * Working with 5 steps of form input
     */

    if (window.location.pathname === '/add-donation/') {
        // transition STEP 1 - STEP 2
        const buttonStep1 = document.querySelector(".step1");
        let chosenCategories;
        buttonStep1.addEventListener("click", (e) => {

            // getting list of chosen categories
            chosenCategories = [];
            const inputs = e.target.parentElement.parentElement.querySelectorAll("input");
            inputs.forEach(input => {
                if (input.checked) {
                    chosenCategories.push(input.value);
                }
            });
        });

        // Transition STEP 2 - STEP 3
        const buttonStep2 = document.querySelector(".step2");
        let bags = 0;

        buttonStep2.addEventListener("click", (e) => {
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

                // if only 1 category was selected, all- and some- lists are the same, so second one is not dispalyed
                if (chosenCategories.length === 1) {
                    institutionsContainerSome.style.display = "none";
                    let h4Element = institutionsContainerSome.previousSibling.previousSibling;
                    h4Element.style.display = "none";
                } else {
                    institutionsContainerSome.style.display = "flex";

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
                displayEmptyContainer(institutionsContainerSome);
            }

            function displayEmptyContainer(container) {
                let infoTag = container.querySelectorAll("h4.text-bg-danger");
                if (infoTag.length === 0) {
                    const infoTag = document.createElement("h4");
                    infoTag.textContent = "Brak wyników";
                    infoTag.setAttribute("class", "text-bg-danger mb-4");
                    infoTag.setAttribute("style", "display: none;");
                    container.appendChild(infoTag);
                }

                let displayedData = [];

                [...container.children].forEach(child => {
                    if (child.style.display !== 'none' && child.tagName === 'DIV') {
                        displayedData.push(child);
                    }
                });
                if (displayedData.length === 0) {
                    const infoTag = container.querySelector("h4.text-bg-danger");
                    infoTag.style.display = "flex";
                } else {
                    const infoTag = container.querySelector("h4.text-bg-danger");
                    infoTag.style.display = "none";
                }
            }


            // collecting and validating number of bags input from STEP 2
            const bagsInput = e.target.parentElement.parentElement.querySelector("input");

            function isNumeric(num) {
                return !isNaN(parseFloat(num)) && isFinite(num);
            }

            // if input in STEP 2 is correct bags will take its value, else stay at 0
            if (isNumeric(bagsInput.value)) {
                let bagsValue = Number(bagsInput.value);
                if (bagsValue > 0) {
                    bags = bagsValue;
                }
            }

            const institutionsContainer = document.querySelector(".data-step-3");

            // Listing institutions in STEP 3 that matches the criteria from STEP 1
            displayInstitutions(institutionsContainer, chosenCategories);
        });

        // transition STEP 3 - STEP 4
        const buttonStep3 = document.querySelector(".step3");
        let chosenInstitution = [];
        buttonStep3.addEventListener("click", e => {

            // collecting chosen institution from STEP 3
            const institutionsContainer = document.querySelector(".data-step-3");
            [...institutionsContainer.querySelectorAll(".form-group--checkbox")].forEach(child => {
                let input = child.querySelector("input");
                if (input.checked) {
                    chosenInstitution[0] = child.querySelector(".title").textContent;
                    chosenInstitution[1] = child.querySelector(".inst-type").textContent;
                }
            });
        });


        // transition STEP 4 - STEP 5
        const buttonStep4 = document.querySelector(".step4");
        buttonStep4.addEventListener("click", e => {

            // collecting all the info from STEP 4
            const formContainer = document.querySelector(".data-step-4");
            const addressInput = formContainer.querySelector("[name='address']");
            const cityInput = formContainer.querySelector("[name='city']");
            const postcodeInput = formContainer.querySelector("[name='postcode']");
            const phoneInput = formContainer.querySelector("[name='phone']");
            const dateInput = formContainer.querySelector("[name='date']");
            const timeInput = formContainer.querySelector("[name='time']");
            const infoInput = formContainer.querySelector("[name='more_info']");

            // displaying data from previous inputs in STEP 5
            const summaryContainer = document.querySelector(".data-step-5");

            // Letting user know if there are any mistakes
            const whatAndHowMany = summaryContainer.querySelector(".what-and-how-many");
            if (chosenCategories.length === 0) {
                whatAndHowMany.textContent = "Wróć do kroku 1 i wybierz poprawną kategorię darów (przynajmniej 1)"
            } else if (bags <= 0) {
                whatAndHowMany.textContent = "Wróć do kroku 2 i wpisz poprawną liczbę worków (więcej niż 0)"
            } else {
                whatAndHowMany.textContent = `Liczba worków: ${Math.ceil(bags)}, dary: ${chosenCategories}`;
            }

            let names = ["Inna organizacja", "Fundacja", "Organizacja pozarządowa", "Lokalna zbiórka"];
            const toWho = summaryContainer.querySelector(".to-who");
            if (!chosenInstitution) {
                toWho.textContent = "Wróć do kroku 3 i wybierz poprawną instytucję (1)";
            } else {
                toWho.textContent = `Obdarowana: ${names[chosenInstitution[1]]} ${chosenInstitution[0]}`;
            }

            const address = summaryContainer.querySelector(".address");
            if (!addressInput.value) {
                address.textContent = "Wróć do kroku 4 i wpisz poprawny adres";
            } else {
                address.textContent = addressInput.value;
            }

            const city = summaryContainer.querySelector(".city");
            if (!cityInput.value) {
                city.textContent = "Wróć do kroku 4 i wpisz poprawne miasto";
            } else {
                city.textContent = cityInput.value;
            }

            const postcode = summaryContainer.querySelector(".postcode");
            if (!postcodeInput.value) {
                postcode.textContent = "Wróć do kroku 4 i wpisz poprawny kod pocztowy";
            } else {
                postcode.textContent = postcodeInput.value;
            }

            const phone = summaryContainer.querySelector(".phone");
            if (!phoneInput.value) {
                phone.textContent = "Wróć do kroku 4 i wpisz poprawny numer telefonu";
            } else {
                phone.textContent = phoneInput.value;
            }

            const date = summaryContainer.querySelector(".date");
            if (!dateInput.value) {
                date.textContent = "Wróć do kroku 4 i wpisz poprawną datę";
            } else {
                date.textContent = dateInput.value;
            }

            const time = summaryContainer.querySelector(".time");
            if (!timeInput.value) {
                time.textContent = "Wróć do kroku 4 i wpisz poprawny czas";
            } else {
                time.textContent = timeInput.value;
            }

            const info = summaryContainer.querySelector(".info");
            if (!infoInput.value) {
                info.textContent = "Brak uwag";
            } else {
                info.textContent = infoInput.value;
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
});


// Help section
// line 1429 in style.css

// function displayResults(section) {
//     let container = section.querySelector(".item-list");
//     let activePageElement = container.parentElement.querySelector(".help--slides-pagination").querySelector(".active");
//     let page = Number(activePageElement.dataset.page);
//     let lowerLimit = (page - 1) * resultsPerPage + 1;
//
//     [...container.children].forEach(function (child) {
//         if (Number(child.classList[0]) >= lowerLimit && Number(child.classList[0]) <= lowerLimit + 4) {
//             child.style.display = "flex";
//         } else {
//             child.style.display = "none";
//         }
//     });
// }
//
// const containerPagination = document.querySelectorAll(".item-pagination > li");
// containerPagination.forEach(function (button) {
//     button.addEventListener("click", function (e) {
//         console.log(e.target)
//         if (![...e.target.classList].includes('active')) {
//             console.log('active', e.target)
//             let toRemove = this.parentElement.parentElement.querySelector(".active");
//             toRemove.classList.remove("active");
//             this.firstChild.classList.add("active");
//             displayResults(this.parentElement.parentElement);
//         }
//     });
// });
//
//
// displayResults(document);