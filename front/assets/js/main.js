/*
	Hyperspace by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function($) {

	var	$window = $(window),
		$body = $('body'),
		$sidebar = $('#sidebar');

	// Breakpoints.
		breakpoints({
			xlarge:   [ '1281px',  '1680px' ],
			large:    [ '981px',   '1280px' ],
			medium:   [ '737px',   '980px'  ],
			small:    [ '481px',   '736px'  ],
			xsmall:   [ null,      '480px'  ]
		});

	// Hack: Enable IE flexbox workarounds.
		if (browser.name == 'ie')
			$body.addClass('is-ie');

	// Play initial animations on page load.
		$window.on('load', function() {
			window.setTimeout(function() {
				$body.removeClass('is-preload');
			}, 100);
		});

	// Forms.

		// Hack: Activate non-input submits.
			$('form').on('click', '.submit', function(event) {

				// Stop propagation, default.
					event.stopPropagation();
					event.preventDefault();

				// Submit form.
					$(this).parents('form').submit();

			});

	// Sidebar.
		if ($sidebar.length > 0) {

			var $sidebar_a = $sidebar.find('a');

			$sidebar_a
				.addClass('scrolly')
				.on('click', function() {

					var $this = $(this);

					// External link? Bail.
						if ($this.attr('href').charAt(0) != '#')
							return;

					// Deactivate all links.
						$sidebar_a.removeClass('active');

					// Activate link *and* lock it (so Scrollex doesn't try to activate other links as we're scrolling to this one's section).
						$this
							.addClass('active')
							.addClass('active-locked');

				})
				.each(function() {

					var	$this = $(this),
						id = $this.attr('href'),
						$section = $(id);

					// No section for this link? Bail.
						if ($section.length < 1)
							return;

					// Scrollex.
						$section.scrollex({
							mode: 'middle',
							top: '-20vh',
							bottom: '-20vh',
							initialize: function() {

								// Deactivate section.
									$section.addClass('inactive');

							},
							enter: function() {

								// Activate section.
									$section.removeClass('inactive');

								// No locked links? Deactivate all links and activate this section's one.
									if ($sidebar_a.filter('.active-locked').length == 0) {

										$sidebar_a.removeClass('active');
										$this.addClass('active');

									}

								// Otherwise, if this section's link is the one that's locked, unlock it.
									else if ($this.hasClass('active-locked'))
										$this.removeClass('active-locked');

							}
						});

				});

		}

	// Scrolly.
		$('.scrolly').scrolly({
			speed: 1000,
			offset: function() {

				// If <=large, >small, and sidebar is present, use its height as the offset.
					if (breakpoints.active('<=large')
					&&	!breakpoints.active('<=small')
					&&	$sidebar.length > 0)
						return $sidebar.height();

				return 0;

			}
		});

	// Spotlights.
		$('.spotlights > section')
			.scrollex({
				mode: 'middle',
				top: '-10vh',
				bottom: '-10vh',
				initialize: function() {

					// Deactivate section.
						$(this).addClass('inactive');

				},
				enter: function() {

					// Activate section.
						$(this).removeClass('inactive');

				}
			})
			.each(function() {

				var	$this = $(this),
					$image = $this.find('.image'),
					$img = $image.find('img'),
					x;

				// Assign image.
					$image.css('background-image', 'url(' + $img.attr('src') + ')');

				// Set background position.
					if (x = $img.data('position'))
						$image.css('background-position', x);

				// Hide <img>.
					$img.hide();

			});

	// Features.
		$('.features')
			.scrollex({
				mode: 'middle',
				top: '-20vh',
				bottom: '-20vh',
				initialize: function() {

					// Deactivate section.
						$(this).addClass('inactive');

				},
				enter: function() {

					// Activate section.
						$(this).removeClass('inactive');

				}
			});

	// Report form
	$(document).ready(function () {
		api_host = "http://localhost:3000"

		function loadOption(add_url, id_html, data_key, all_plateform = false) {
			fetch(api_host + add_url) // Remplace par l'URL de ton API
			.then(response => response.json())
				.then(data => {
					$(id_html).empty();

					if (all_plateform) {
						$(id_html).append(new Option("Toute les Plateform", ""));
					}

					data?.[data_key].forEach(level => {
						$(id_html).append(new Option(level.name, level.id));
					});
				})
			.catch(error => {
				console.error('Erreur lors du chargement des types de harcèlement :', error);
			});
		}
		loadOption("/level/", "#severity", "levels")
		loadOption("/harassment_type/", "#harassment-type", "harassment_types")
		loadOption("/platform/", "#platform", "platforms")
		loadOption("/platform/", "#platformfilter", "platforms", true)

		function loadTestimonies(add_url, username = "", platform = "", id_html = "#testimonals") {
			filter_message = username != "" ? `?username=${encodeURIComponent(username)}` : ""
			platform_filter = platform != "" ? `platform=${encodeURIComponent(platform)}` : ""
			sep = "?"
			if (username != "") {
				sep = platform != "" ? "&" : ""
			}
			filter_message = username == "" && platform == "" ? "" : filter_message + sep + platform_filter
			console.log(filter_message)
			const url = api_host + add_url + filter_message;
			fetch(url) // Remplace par l'URL de ton API
			.then(response => response.json())
				.then(data => {
					$(id_html).empty();

					Object.keys(data).forEach(stalker_name => {
						$(id_html).append(`<h3>${stalker_name}</h3>`)
						data?.[stalker_name].forEach(message => {
							$(id_html).append(`<blockquote>${message?.description}</blockquote>`);
						})
					})
				})
			.catch(error => {
				console.error('Erreur lors du chargement des types de harcèlement :', error);
			});
		}

		loadTestimonies("/message/by_stalker_platform")

		$('#filter-button').on('click', function (event) {
			event.preventDefault(); // Empêche le rechargement de la page

			// Récupération des valeurs des filtres
			const username = $('#usernamefilter').val(); // Utilise le bon id du filtre
			const platform = $('#platformfilter').val(); // Utilise le bon id du filtre

			// Recharge les témoignages avec les filtres
			loadTestimonies("/message/by_stalker_platform", username, platform);
		});

		$('#submit-report').on('click', function (event) {

			event.preventDefault(); // Empêche le rechargement de la page

			// Récupération des données du formulaire
			var formData = {
				"stalker_name": $('#username').val(),
				"description": $('#description').val(),
				"level_id": parseInt($('#severity').val()),
				"harassment_type_id": parseInt($('#harassment-type').val()),
				"platform_id": parseInt($('#platform').val())
			}


			// Récupération du fichier preuve (s'il y en a un)
			var proofFile = $('#proof')[0].files[0];
			if (proofFile) {
				formData.append('proof', proofFile);
			}

			// Validation de la checkbox
			if (!$('#terms').is(':checked')) {
				alert("Vous devez accepter les conditions d'utilisation et la politique de confidentialité.");
				return;
			}

			$.ajax({
				url: api_host + "/message/", // Remplace par l'URL de ton API
				type: 'POST',
				data: JSON.stringify(formData),
				processData: false,
				contentType: 'application/json',
				success: function (response) {
					if (response?.success) {
						alert("Votre signalement a été envoyé avec succès.");
						$('form')[0].reset();
						location.reload();
					} else {
						alert("Une erreur est survenue lors de l'envoi du signalement.");
					}
				},
				error: function (xhr, status, error) {
					console.log(xhr, status, error)
					alert("Une erreur est survenue : " + error);
				}
			});
		})
	})

})(jQuery);