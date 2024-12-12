(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 45) {
            $('.navbar').addClass('sticky-top shadow-sm');
        } else {
            $('.navbar').removeClass('sticky-top shadow-sm');
        }
    });
    
    
    // Dropdown on mouse hover
    const $dropdown = $(".dropdown");
    const $dropdownToggle = $(".dropdown-toggle");
    const $dropdownMenu = $(".dropdown-menu");
    const showClass = "show";
    
    $(window).on("load resize", function() {
        if (this.matchMedia("(min-width: 992px)").matches) {
            $dropdown.hover(
            function() {
                const $this = $(this);
                $this.addClass(showClass);
                $this.find($dropdownToggle).attr("aria-expanded", "true");
                $this.find($dropdownMenu).addClass(showClass);
            },
            function() {
                const $this = $(this);
                $this.removeClass(showClass);
                $this.find($dropdownToggle).attr("aria-expanded", "false");
                $this.find($dropdownMenu).removeClass(showClass);
            }
            );
        } else {
            $dropdown.off("mouseenter mouseleave");
        }
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Facts counter
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });



    
    function toggleTabContent(tabId) {
        const $tabButton = $(`[onclick="toggleTabContent('${tabId}')"]`);
        const $content = $(`#${tabId}-content`);
        
        $tabButton.toggleClass('active');
        $content.toggleClass('show fade');
    }


    $(document).ready(function() {
        $('#menu-search-form').submit(function(event) {
            event.preventDefault(); // Prevent the default form submission
            
            // Collect form data (if necessary)
            console.log("Form submitted");
            
            // You can do additional work here before submitting, like sending AJAX requests
            
            // After you're ready, submit the form
            this.submit();  // This will trigger the form submission
        });
    });
    
    
    
    function submitForm() {
        var form = document.getElementById("menu-search-form");
        print("hi"+form)
        form.submit();
    }
    

    // Modal Video
    $(document).ready(function () {
        var $videoSrc;
        $('.btn-play').click(function () {
            $videoSrc = $(this).data("src");
        });
        console.log($videoSrc);

        $('#videoModal').on('shown.bs.modal', function (e) {
            $("#video").attr('src', $videoSrc + "?autoplay=1&amp;modestbranding=1&amp;showinfo=0");
        })

        $('#videoModal').on('hide.bs.modal', function (e) {
            $("#video").attr('src', $videoSrc);
        })
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        center: true,
        margin: 24,
        dots: true,
        loop: true,
        nav : false,
        responsive: {
            0:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:3
            }
        }
    });
    
})(jQuery);

// Contact form submission handler
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    const submitButton = document.getElementById('submitButton');
    const formMessage = document.getElementById('formMessage');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Disable submit button and show loading state
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Sending...';
            
            // Get form data
            const formData = new FormData(contactForm);
            
            // Submit form
            fetch('/submit_feedback', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                // Show success/error message
                formMessage.style.display = 'block';
                formMessage.className = data.success ? 
                    'alert alert-success mt-3' : 'alert alert-danger mt-3';
                formMessage.textContent = data.message;
                
                // Reset form on success
                if (data.success) {
                    contactForm.reset();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                formMessage.style.display = 'block';
                formMessage.className = 'alert alert-danger mt-3';
                formMessage.textContent = 'An error occurred. Please try again later.';
            })
            .finally(() => {
                // Re-enable submit button
                submitButton.disabled = false;
                submitButton.innerHTML = 'Send Message';
                
                // Hide message after 5 seconds
                setTimeout(() => {
                    formMessage.style.display = 'none';
                }, 5000);
            });
        });
    }
});

function loadTrendingFavorites() {
    const container = document.getElementById('trending-favorites');
    if (!container) return;

    container.innerHTML = `
        <div class="col-12 text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;

    fetch('/api/trending-favorites')
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (data.status === 'success' && data.favorites && data.favorites.length > 0) {
                container.innerHTML = data.favorites.map((dish, index) => `
                    <div class="col-lg-4 col-md-6 wow fadeInUp" data-wow-delay="${0.1 + (index * 0.2)}s">
                        <div class="service-item rounded pt-3">
                            <div class="p-4">
                                <h5 class="mb-3">${dish.name}</h5>
                                <div class="d-flex align-items-center">
                                    <i class="fa fa-heart text-primary me-2"></i>
                                    <span>${dish.favorites} students love this</span>
                                </div>
                            </div>
                        </div>
                    </div>
                `).join('');
            } else {
                container.innerHTML = `
                    <div class="col-12 text-center">
                        <div class="p-4">
                            <i class="fa fa-heart text-primary mb-3" style="font-size: 2rem;"></i>
                            <p class="text-muted">Ready to discover favorite dishes? Browse our menu and start saving your favorites!</p>
                            <a href="/menu" class="btn btn-primary mt-3">
                                <i class="fa fa-cutlery me-2"></i>Browse Menu
                            </a>
                        </div>
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error('Error loading trending favorites:', error);
            container.innerHTML = `
                <div class="col-12 text-center">
                    <div class="p-4">
                        <i class="fa fa-exclamation-circle text-danger mb-3" style="font-size: 2rem;"></i>
                        <p class="text-danger">Unable to load trending favorites</p>
                        <button onclick="loadTrendingFavorites()" class="btn btn-primary mt-3">
                            <i class="fa fa-refresh me-2"></i>Try Again
                        </button>
                    </div>
                </div>
            `;
        });
}

document.addEventListener('DOMContentLoaded', function() {
    loadTrendingFavorites();
});

