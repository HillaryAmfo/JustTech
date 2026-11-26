"""Lightweight site translation (English -> French).

Keys are the English source strings used in templates; the ``tr``
template filter swaps them for the French equivalent when the visitor's
language is French. Database-driven content (services, testimonials,
FAQ, portfolio) is shown as entered in the admin.
"""

SUPPORTED_LANGS = ('en', 'fr')

FR = {
    # Header / nav
    'About': 'À propos',
    'Services': 'Services',
    'Portfolio': 'Réalisations',
    'Learning': 'Apprentissage',
    'Contact': 'Contact',
    'Log in': 'Connexion',
    'Log out': 'Déconnexion',
    'Book now': 'Réserver',
    'Language': 'Langue',
    'English': 'Anglais',
    'Français': 'Français',

    # Hero eyebrow
    'Audio • Technology • Training': 'Audio • Technologie • Formation',
    'Professional Audio & Visual Services': 'Services professionnels Audio & Visuel',
    'Training & Learning': 'Formation & Apprentissage',

    # Hero sub-copy + CTAs
    'Event sound, sound engineering, streaming systems, custom PCs and hands-on training — designed, built and tuned by people who care about the details.':
        'Sonorisation d’événements, ingénierie du son, systèmes de streaming, PC sur mesure et formation pratique — conçus, construits et réglés par des gens qui aiment le détail.',
    'Book Now': 'Réserver',
    'Explore Services': 'Découvrir nos services',
    'Explore Learning': 'Découvrir la formation',

    # Stats
    'By the numbers': 'En chiffres',
    'The numbers behind the sound.': 'Les chiffres derrière le son.',
    'Every number is a room we’ve shaped, a mix we’ve run or a skill we’ve handed over — real work, no filler.':
        'Chaque chiffre est une salle qu’on a façonnée, un mix qu’on a dirigé ou une compétence transmise — du vrai travail, sans blabla.',
    'See the work behind the numbers': 'Voir le travail derrière les chiffres',
    'Projects Completed': 'Projets réalisés',
    'Events, studios, installs & streaming setups': 'Événements, studios, installations & systèmes de streaming',
    'Students Trained': 'Apprenants formés',
    'Engineers, artists & curious beginners': 'Ingénieurs, artistes & curieux débutants',
    'Client Satisfaction': 'Satisfaction client',
    'Support Available': 'Support disponible',
    'Repeat events, referrals & long-term clients': 'Événements récurrents, recommandations & clients fidèles',
    'Serving Since': 'En activité depuis',
    'Sound-first from day one — and still tuned': 'Le son avant tout depuis le début — toujours au point',

    # Portfolio page
    'Our work': 'Notre travail',
    'Small team,': 'Petite équipe,',
    'big results.': 'grands résultats.',
    'See the work': 'Voir le travail',
    'Audio systems, streams, events and builds — designed, wired and tuned end to end.':
        'Systèmes audio, streams, événements et builds — conçus, câblés et réglés de bout en bout.',
    'Projects shipped': 'Projets livrés',
    'Services covered': 'Services couverts',
    'Done in-house, end to end': 'Faits maison, de bout en bout',
    'Recent work: live concerts, recording, streaming and more.':
        'Travaux récents : concerts live, enregistrement, streaming et plus.',

    # Services section
    'We design, build and support the systems behind great sound and video.':
        'Nous concevons, construisons et maintenons les systèmes derrière un grand son et une belle image.',
    'From a single live event to a full studio or streaming setup, our work is practical, reliable and built around how you actually use it.':
        'D’un simple événement live à un studio complet ou un système de streaming, notre travail est pratique, fiable et pensé pour votre usage réel.',
    'View all services': 'Voir tous les services',
    'Book': 'Réserver',
    'Add services in the admin panel.': 'Ajoutez des services dans le panneau d’administration.',

    # Event audio
    'Event Audio': 'Audio événementiel',
    'You run the event.<br>We handle the sound.': 'Vous gérez l’événement.<br>Nous gérons le son.',
    'From soundcheck to the last song, we take care of the technical side — so the room sounds the way it should and your team can focus on the event.':
        'Du soundcheck à la dernière chanson, nous gérons tout le côté technique — pour que la salle sonne comme il faut et que votre équipe se concentre sur l’événement.',
    'Setup': 'Installation',
    'System tuning': 'Réglage système',
    'Soundcheck': 'Soundcheck',
    'Mixing & monitoring': 'Mixage & monitoring',
    'Live operation': 'Exploitation en direct',
    'Technical support': 'Support technique',
    'Breakdown': 'Démontage',
    'Concerts, conferences, churches, corporate events, weddings and private events — any space that needs professional sound.':
        'Concerts, conférences, églises, événements d’entreprise, mariages et événements privés — tout espace qui a besoin d’un son professionnel.',
    'Book event sound': 'Réserver le son d’événement',
    'Explore services': 'Découvrir les services',

    # Featured work
    'Work': 'Travaux',
    'Recent work': 'Travaux récents',
    'View all work': 'Voir tous les travaux',
    'Featured work appears here once projects are added in the admin panel.':
        'Les travaux vedettes apparaissent ici une fois les projets ajoutés dans le panneau d’administration.',

    # Learning
    'Learn the craft behind the sound.': 'Apprenez le métier derrière le son.',
    'We teach what we do every day — hands-on, practical, and at your pace. Whether you want to play an instrument or run a mix, the quickest way is to do it.':
        'Nous enseignons ce que nous faisons chaque jour — pratique et à votre rythme. Que vous vouliez jouer d’un instrument ou diriger un mix, le plus rapide est de le faire.',
    'Music': 'Musique',
    'Piano, guitar & instruments': 'Piano, guitare & instruments',
    'Lessons for every level — play real music from your first session. Instruments are provided, so just book and show up.':
        'Cours pour tous les niveaux — jouez de la vraie musique dès la première séance. Les instruments sont fournis, réservez et venez.',
    'One-on-one lessons at your level': 'Cours particuliers à votre niveau',
    'Instruments and gear provided': 'Instruments et matériel fournis',
    'From absolute beginner to advanced': 'Du débutant complet à l’avancé',
    'Explore music lessons': 'Découvrir les cours de musique',
    'Technical': 'Technique',
    'Sound engineering & live audio': 'Ingénierie du son & audio live',
    'Mixing, sound systems and streaming — taught on real equipment so you finish confident enough to run the show.':
        'Mixage, systèmes de son et streaming — enseignés sur du vrai équipement pour repartir assez confiant pour diriger le spectacle.',
    'Sound engineering & live mixing': 'Ingénierie du son & mixage live',
    'Audio systems & streaming setups': 'Systèmes audio & installations de streaming',
    'One-on-one and structured training': 'Formation particulière et structurée',
    'Explore technical training': 'Découvrir la formation technique',
    'Book a lesson': 'Réserver un cours',
    'Explore learning': 'Découvrir la formation',

    # Why JustTech
    'Why JustTech': 'Pourquoi JustTech',
    'Built on the details': 'Construit sur le détail',
    'We treat every project like it matters — because the room always hears the difference.':
        'Chaque projet compte pour nous — car la salle entend toujours la différence.',
    'Detail matters': 'Le détail compte',
    'Every setup is designed, built and tested carefully before it goes live.':
        'Chaque installation est conçue, construite et testée avec soin avant d’être mise en service.',
    'Real-world experience': 'L’expérience du terrain',
    'Systems are made for actual venues, events and workflows — not just brochure specs.':
        'Les systèmes sont faits pour de vrais lieux, événements et flux de travail — pas seulement pour la fiche technique.',
    'Built for you': 'Pensé pour vous',
    'Recommendations match your use case and budget, rather than simply selling equipment.':
        'Nos recommandations correspondent à votre besoin et à votre budget, plutôt que de simplement vendre du matériel.',
    'Support beyond installation': 'Un support au-delà de l’installation',
    'We stay involved after the setup goes in — running events, training teams and troubleshooting.':
        'Nous restons impliqués après l’installation — événements, formation des équipes et dépannage.',
    'Practical learning': 'Formation pratique',
    'Training is hands-on — you leave behind the gear and knowing how to use it.':
        'La formation est pratique — vous repartez avec l’équipement et le savoir-faire.',
    'Tell us what you need': 'Dites-nous ce dont vous avez besoin',
    'We design the right setup': 'Nous concevons la bonne installation',
    'We build and configure': 'Nous construisons et configurons',
    'We test and soundcheck': 'Nous testons et faisons le soundcheck',
    'We support the experience': 'Nous accompagnons l’expérience',

    # Testimonials + FAQ
    'Testimonials': 'Témoignages',
    'What people say': 'Ce qu’ils disent',
    'Previous testimonial': 'Témoignage précédent',
    'Next testimonial': 'Témoignage suivant',
    'Questions, answered': 'Questions, réponses',

    # Final CTA
    'Have a project in mind?': 'Un projet en tête ?',
    'Tell us what you’re building, planning or trying to learn — we’ll take it from there.':
        'Dites-nous ce que vous construisez, planifiez ou souhaitez apprendre — nous nous occupons du reste.',
    'Contact Us': 'Contactez-nous',

    # Footer
    "Let's work together.": 'Travaillons ensemble.',
    'A Canadian-based audio & visual company that designs, builds and teaches. We bring professional sound, streaming and production to the people who need it.':
        'Une entreprise canadienne d’audio & visuel qui conçoit, construit et forme. Nous apportons du son, du streaming et de la production professionnels à ceux qui en ont besoin.',
    'Navigate': 'Navigation',
    'Capabilities': 'Expertises',
    'Reach Us': 'Nous contacter',
    'Portfolio': 'Portfolio',
    'Get Started': 'Démarrer',
    'Connect': 'Suivez-nous',
    'Start a project': 'Démarrer un projet',
    'Live Sound & Events': 'Son live & événements',
    'Sound Engineering': 'Ingénierie du son',
    'Streaming Systems': 'Systèmes de streaming',
    'Custom PCs & Builds': 'PC sur mesure',
    'Studio Installation': 'Installation de studio',
    'Hands-on Training': 'Formation pratique',
    'Toronto, Ontario, Canada': 'Toronto, Ontario, Canada',
    'All rights reserved.': 'Tous droits réservés.',
    'Privacy Policy': 'Politique de confidentialité',
    'Terms of Service': 'Conditions d’utilisation',

    # ------------------------------------------------#
    # About hero
    'About JustTech': 'À propos de JustTech',
    'REC': 'ENR',
    'LIVE SOUND': 'SON LIVE',
    'STREAMING': 'STREAMING',
    'CUSTOM BUILDS': 'CONSTRUCTIONS SUR MESURE',
    'The people · not just the gear': 'Les personnes · pas seulement le matériel',
    'Meet the people': 'Rencontrez les personnes',
    'behind': 'derrière',
    'the': 'le',
    'sound.': 'son.',
    'Meet the team': 'Rencontrer l’équipe',
    'Our story': 'Notre histoire',
    'Projects': 'Projets',
    'Sound should': 'Le son devrait',
    'feel good': 'sonner aussi bien',
    'as it sounds.': 'qu’il en a l’air.',
    'Just Tech started as a small studio with one mixing console and a belief: that professional-grade audio and visual technology should be within reach for everyone.':
        'Just Tech a commencé comme un petit studio avec une console de mixage et une conviction : la technologie audio et visuelle de niveau professionnel devrait être à la portée de tous.',
    'Today we design and build sound systems, streaming setups, and custom PCs — and we teach the next generation of creators and technicians.':
        'Aujourd’hui, nous concevons et construisons des systèmes de son, des configurations de streaming et des PC sur mesure — et nous formons la prochaine génération de créateurs et de techniciens.',
    'Our Story': 'Notre histoire',
    'People': 'Personnes',
    'Technology': 'Technologie',
    'Creativity': 'Créativité',
    'Design · Build · Teach': 'Concevoir · Construire · Former',

    # About story
    'The studio where it all began.': 'Le studio où tout a commencé.',
    'It started in a room in Ontario.': 'Tout a commencé dans une salle en Ontario.',
    "JustTech began with a single mixing console, one small room in Ontario and a simple belief — that professional sound should be within everyone's reach.":
        'JustTech a commencé avec une seule console de mixage, une petite salle en Ontario et une conviction simple — le son professionnel devait être à la portée de tous.',
    'A sound mixing console in the studio': 'Une console de mixage en studio',
    'WHERE IT BEGAN': 'LÀ OÙ TOUT A COMMENCÉ',
    'One room.': 'Une seule pièce.',
    'The JustTech difference': 'La différence JustTech',
    'what makes us': 'ce qui nous rend',
    'different': 'différents',
    'What makes us different': 'Ce qui nous rend différents',
    "Because we design, build and teach — the person who plans your system is the same one who wires it, tunes it and trains your team. One room, one team, end to end.":
        'Parce que nous concevons, construisons et formons — la personne qui planifie votre système est la même qui le câble, le règle et forme votre équipe. Une pièce, une équipe, de bout en bout.',
    'Just Tech started with a single mixing console and a simple belief: good gear should be accessible, understood and used well.':
        'Just Tech a commencé avec une seule console de mixage et une conviction simple : le bon matériel doit être accessible, compris et bien utilisé.',
    'Today that same hands-on attitude runs through everything we do — live sound, streaming, video, custom PCs and the training we offer.':
        'Aujourd’hui, cette même approche concrète traverse tout ce que nous faisons — son live, streaming, vidéo, PC sur mesure et la formation que nous proposons.',
    'MIXING • LIVE': 'MIXAGE • DIRECT',

    # About values
    'What we value': 'Ce qui compte pour nous',
    'Simple ideas, done properly.': 'Des idées simples, bien réalisées.',
    'Design': 'Concevoir',
    'Every installation is designed around the room and the people who use it.':
        'Chaque installation est conçue en fonction de la salle et des personnes qui l’utilisent.',
    'Build': 'Construire',
    'Sound, streaming and systems built on real gear — tested before they go live.':
        'Son, streaming et systèmes construits sur du vrai matériel — testés avant la mise en service.',
    'Teach': 'Former',
    'We teach what we do every day — practical, hands-on and at your pace.':
        'Nous enseignons ce que nous faisons chaque jour — pratique et à votre rythme.',

    # About team
    'Meet Our Team': 'Rencontrer notre équipe',
    'The people behind the console.': 'Les personnes derrière la console.',
    'Team members will appear here once added in the admin panel.':
        'Les membres de l’équipe apparaîtront ici une fois ajoutés dans le panneau d’administration.',

    # About testimonials + CTA
    'Client testimonials appear here once added in the admin panel.':
        'Les témoignages clients apparaîtront ici une fois ajoutés dans le panneau d’administration.',
    'Work With Us': 'Travaillons ensemble',
    'Ready to bring your audio and visual projects to life with our expert team?':
        'Prêt à donner vie à vos projets audio et visuels avec notre équipe experte ?',
    'Schedule Consultation': 'Planifier une consultation',
    'Contact Our Team': 'Contactez notre équipe',

    # About team — nav + language-aware member data
    'Browse team members': 'Parcourir les membres',
    'Previous team member': 'Membre d’équipe précédent',
    'Next team member': 'Membre d’équipe suivant',
    'Team member index': 'Index des membres',
    'Meet the JustTech team': 'Rencontrez l’équipe JustTech',

    # About — our journey milestones
    'Our journey': 'Notre parcours',
    'Since 2018, growing with the sound.': 'Depuis 2018, on grandit avec le son.',
    'The studio is born.': 'La naissance du studio.',
    'One mixing console, a small room and the belief that great sound should be accessible to everyone.':
        'Une console de mixage, une petite pièce et la conviction qu’un grand son doit être accessible à tous.',
    'Streaming & content.': 'Streaming & contenu.',
    'We start producing live streams for churches, schools and events across Canada.':
        'Nous lançons les diffusions live pour les églises, écoles et événements partout au Canada.',
    'Custom builds.': 'PC sur mesure.',
    'Custom PCs, installations and system design join the studio lineup.':
        'Les PC sur mesure, les installations et la conception de systèmes rejoignent le studio.',
    'Training academy.': 'Académie de formation.',
    'Hands-on courses in sound engineering, streaming and production.':
        'Des cours pratiques d’ingénierie du son, de streaming et de production.',

    # About — get in touch
    'Get in touch': 'Prenons contact',
    'Visit us, call us or just say hello.': 'Rendez-nous visite, appelez-nous ou dites bonjour.',
    'No project is too small — tell us what you are planning and we will take it from there.':
        'Aucun projet n’est trop petit — dites-nous ce que vous prévoyez et nous nous occupons du reste.',
    'Visit the studio': 'Visiter le studio',
    'Call us': 'Appelez-nous',
    'Email us': 'Écrivez-nous',
    'Working hours': 'Heures d’ouverture',
    'Mon – Fri: 9:00 – 18:00': 'Lun – Ven : 9 h – 18 h',
    'Sat: 10:00 – 16:00': 'Sam : 10 h – 16 h',

    # Contact page
    'Drop by, call or send a note — whatever works best for you.':
        'Passez nous voir, appelez-nous ou écrivez — comme vous voulez.',
    'Send a message': 'Envoyer un message',
    'Find the studio': 'Trouver le studio',
    'Response time': 'Délai de réponse',
    'Usually within one working day.': 'Généralement sous un jour ouvrable.',
    'Ways to reach us': 'Pour nous joindre',
    'Contact form': 'Formulaire de contact',
    'Studio & offices': 'Studio et bureaux',
    'Our studio': 'Notre studio',
    'Prefer to talk it through first?': 'Vous préférez en parler d’abord ?',
    'Book a free consultation': 'Réserver une consultation gratuite',
    'Live outside the area? We work across Canada.':
        'Hors de la région ? Nous travaillons partout au Canada.',
    'Your message has been received.': 'Votre message a bien été reçu.',
    'Send message': 'Envoyer le message',
    'Based in Barrie, Ontario — serving Canada.':
        'Basés à Barrie, en Ontario — au service du Canada.',
    'Aerial view of our studio on the shores of Kempenfelt Bay, Lake Simcoe.':
        'Vue aérienne de notre studio sur les rives de la baie Kempenfelt, au bord du lac Simcoe.',
    'Frequently asked questions': 'Questions fréquemment posées',
    'Common questions': 'Questions fréquentes',

    # Contact page rework — Azubi-style sign-in band
    'Client access': 'Espace client',
    'Sign in to continue.': 'Connectez-vous pour continuer.',
    'Track requests, manage your session bookings and receive studio updates from one place.':
        'Suivez vos demandes, gérez vos réservations de session et recevez les actualités du studio au même endroit.',
    'Sign in with Google': 'Se connecter avec Google',
    'Sign in with Microsoft': 'Se connecter avec Microsoft',
    'Sign in with Apple ID': 'Se connecter avec Apple ID',
    'or': 'ou',
    'Continue with email': 'Continuer avec l’e-mail',
    'Continue with __PROVIDER__? Not yet — but your email works today.':
        'Continuer avec __PROVIDER__ ? Pas encore — mais votre e-mail fonctionne dès aujourd’hui.',
    'IN THE STUDIO': 'EN STUDIO',
    'Session 024 — Keys over the first verse': 'Session 024 — Claviers sur le premier couplet',
    'Keyboard · Guitar · Studio': 'Clavier · Guitare · Studio',

    # Contact page rework — Agbedus-style get in touch + action cards
    'Talk to JustTech.': 'Parlez à JustTech.',
    'Tell us about the track, the session or the room — not the technical solution. We will read it properly and suggest a practical next step.':
        'Parlez-nous du morceau, de la session ou de la salle — pas de la solution technique. Nous lisons tout attentivement et suggérons une prochaine étape concrète.',
    'Address': 'Adresse',
    'Phone': 'Téléphone',
    'Book a call': 'Réserver un appel',
    'Email the studio': 'Écrire au studio',
    'Chat with us on WhatsApp': 'Discutez avec nous sur WhatsApp',
    'Follow Us': 'Suivez-nous',
    'Hire the band': 'Engagez le groupe',
    'Session keyboard & guitar for the song you are about to produce — played, recorded and honed in your studio.':
        'Claviers & guitares de session pour le morceau que vous vous apprêtez à produire — joués, enregistrés et peaufinés dans votre studio.',
    'Start a session': 'Lancer une session',
    'Book studio time': 'Réserver du temps studio',
    'Track, mix and master in a room tuned for real results — by the hour or by the day.':
        'Enregistrez, mixez et masterisez dans une salle réglée pour de vrais résultats — à l’heure ou à la journée.',
    'Check availability': 'Vérifier les disponibilités',
    'Sessions, installs, builds or a message that does not fit a box — send it and we will take it from there.':
        'Sessions, installations, montages ou un simple message qui ne rentre dans aucune case — écrivez-nous et nous nous occupons du reste.',
    'Piano, guitar and audio lessons — hands-on, at your pace, on studio gear.':
        'Cours de piano, de guitare et d’audio — pratique, à votre rythme, sur du matériel de studio.',
    'Explore lessons': 'Découvrir les cours',

    # Contact page rework — Azubi portal sign-in card
    'Sign in': 'Se connecter',
    'Continue to your client space.': 'Continuez vers votre espace client.',
    'Your next session starts here.': 'Votre prochaine session commence ici.',
    'Book studio time, track requests and keep your projects moving — all in one place.':
        'Réservez du temps studio, suivez vos demandes et gardez vos projets en mouvement — tout au même endroit.',
    'Email address': 'Adresse e-mail',
    'Password': 'Mot de passe',
    'Forgot Password?': 'Mot de passe oublié ?',
    'Sign In': 'Connexion',
    'Not having an account?': 'Vous n’avez pas de compte ?',
    'Request access': 'Demander un accès',
    'Register': 'S’inscrire',
    'Log in': 'Se connecter',
    'Create your account': 'Créer votre compte',
    'Tell us who you are and what you want to do.': 'Dites-nous qui vous êtes et ce que vous souhaitez faire.',
    'I am here for': 'Je suis là pour',
    'Learning': 'Apprendre',
    'Book a studio session': 'Réserver une session studio',
    'Events & production': 'Événements & production',
    'Something else': 'Autre chose',
    'Full name': 'Nom complet',
    'Confirm password': 'Confirmer le mot de passe',
    'Show password': 'Afficher le mot de passe',
    'Hide password': 'Masquer le mot de passe',
    'Create account': 'Créer le compte',
    'Already have an account?': 'Vous avez déjà un compte ?',
    'One account for everything.': 'Un seul compte pour tout.',
    'Register for lessons, book studio sessions and keep your projects moving — all from your JustTech space.':
        'Inscrivez-vous aux cours, réservez des sessions studio et gardez vos projets en mouvement — depuis votre espace JustTech.',
    'JOIN THE CLUB': 'REJOIGNEZ LE CLUB',
    'COLLABORATE & GROW': 'COLLABOREZ & PROGRESSEZ',
    'An account with this email already exists.': 'Un compte existe déjà avec cette adresse e-mail.',
    'Passwords do not match.': 'Les mots de passe ne correspondent pas.',
    'This password is too short. It must contain at least 8 characters.':
        'Ce mot de passe est trop court. Il doit contenir au moins 8 caractères.',
    'This password is too common.': 'Ce mot de passe est trop courant.',
    'This password is entirely numeric.': 'Ce mot de passe est entièrement numérique.',
    'The password is too similar to the username.': 'Le mot de passe est trop similaire à l’adresse e-mail.',
    'The password is too similar to the first name.': 'Le mot de passe est trop similaire au nom.',
    'The password is too similar to the email address.': 'Le mot de passe est trop similaire à l’adresse e-mail.',
    'You must agree to the Terms and Privacy Policy to continue.':
        'Vous devez accepter les Conditions et la Politique de confidentialité pour continuer.',

    # Register page — provider sign-up
    'Sign up with Google': 'S’inscrire avec Google',
    'Sign up with Microsoft': 'S’inscrire avec Microsoft',
    'Sign up with Apple ID': 'S’inscrire avec Apple ID',
    'or sign up with email': 'ou inscrivez-vous avec votre e-mail',
    'I agree to the JustTech': 'J’accepte les Conditions',
    'Terms': 'Conditions',
    'and': 'et la',
    'Privacy Policy': 'Politique de confidentialité',
    'What would you like to learn?': 'Qu’aimeriez-vous apprendre ?',
    'What type of session?': 'Quel type de session ?',
    'Recording, mixing or rehearsal?': 'Enregistrement, mixage ou répétition ?',
    'What are you planning?': 'Que prévoyez-vous ?',
    'Worship, concert, live stream...': 'Culte, concert, diffusion en direct...',
    'Anything we should know (optional)': 'Que devrions-nous savoir (facultatif)',
    'Tell us a little more': 'Parlez-nous un peu plus',

    # Password reset flow
    'Forgot password': 'Mot de passe oublié',
    'Forgot your password?': 'Mot de passe oublié ?',
    'Enter your account email and we will send you a link to set a new password.':
        'Saisissez l’e-mail de votre compte et nous vous enverrons un lien pour définir un nouveau mot de passe.',
    'Send reset link': 'Envoyer le lien de réinitialisation',
    'Remembered it?': 'Vous vous souvenez de votre mot de passe ?',
    'Back to login': 'Retour à la connexion',
    'Check your email': 'Vérifiez votre e-mail',
    'If an account exists for that address, a password reset link is on its way. Check your inbox (and spam folder).':
        'Si un compte existe pour cette adresse, un lien de réinitialisation est en route. Vérifiez votre boîte de réception (et vos spams).',
    'Development link (DEBUG only)': 'Lien de développement (DEBUG uniquement)',
    'Try another email': 'Essayer une autre adresse e-mail',
    'Set a new password': 'Définir un nouveau mot de passe',
    'Choose a strong password you have not used for this account before.':
        'Choisissez un mot de passe fort que vous n’avez jamais utilisé pour ce compte.',
    'New password': 'Nouveau mot de passe',
    'Confirm new password': 'Confirmer le nouveau mot de passe',
    'Save new password': 'Enregistrer le nouveau mot de passe',
    'Invalid reset link': 'Lien de réinitialisation invalide',
    'This link is invalid or expired': 'Ce lien est invalide ou a expiré',
    'Password reset links work once and expire after a day. Request a fresh one to continue.':
        'Les liens de réinitialisation ne sont valables qu’une fois et expirent après une journée. Demandez un nouveau lien pour continuer.',
    'Request a new link': 'Demander un nouveau lien',
    'Password updated': 'Mot de passe mis à jour',
    'Your password has been changed. You can now log in with it.':
        'Votre mot de passe a été modifié. Vous pouvez maintenant vous connecter avec.',
    'Log in with new password': 'Se connecter avec le nouveau mot de passe',

    # Login page
    'Log out': 'Se déconnecter',
    'Authorised access': 'Accès autorisé',
    'Welcome back': 'Bon retour',
    'Access is provided to authorised users.': 'L’accès est réservé aux utilisateurs autorisés.',
    'Username': 'Nom d’utilisateur',
    'Your username': 'Votre nom d’utilisateur',
    'Your password': 'Votre mot de passe',
    "Don't have an account?": 'Vous n’avez pas de compte ?',
    'Create one': 'Créer un compte',
    'in a minute.': 'en une minute.',

    # Get-in-touch destination pages
    'SEND A MESSAGE': 'ENVOYER UN MESSAGE',
    'Send a message': 'Envoyer un message',
    'Tell us what you need.': 'Dites-nous ce dont vous avez besoin.',
    'We read everything.': 'Nous lisons tout.',
    'Your message': 'Votre message',
    'Lets pick up a conversation. Our inbox, your words.':
        'Ouvrons la conversation. Notre boîte de réception, vos mots.',
    'Studio session': 'Session studio',
    'Sound setup': 'Installation sonore',
    'Custom build': 'Montage sur mesure',
    'Live event': 'Événement en direct',
    'Subject': 'Sujet',
    'Message': 'Message',
    'Your name': 'Votre nom',
    'Tell us about your project or question.': 'Parlez-nous de votre projet ou de votre question.',
    'Next steps': 'Prochaines étapes',
    'NEXT STEPS': 'PROCHAINES ÉTAPES',
    'What happens next?': 'Et ensuite ?',
    'We read it': 'Nous le lisons',
    'A real person reads every message — usually the same day.':
        'Une vraie personne lit chaque message — généralement le jour même.',
    'We reply': 'Nous répondons',
    'A clear answer or a request for the last details — no jargon.':
        'Une réponse claire ou une demande de derniers détails — sans jargon.',
    'We get moving': 'Nous passons à l’action',
    'Booked, built, installed — whatever the next step is, you get it.':
        'Réservé, monté, installé — quelle que soit la prochaine étape, elle sera faite.',

    # Hire the band page
    'HIRE THE BAND': 'ENGAGEZ LE GROUPE',
    'Session players for your record.': 'Des musiciens de session pour votre disque.',
    'Book the players': 'Réserver les musiciens',
    "Track-ready in one session.": 'Prêt à enregistrer en une session.',
    'Real performance, real gear, real takes — arranged around your song before the red light goes on.':
        'De vraies performances, du vrai matériel, de vraies prises — arrangées autour de votre chanson avant que le voyant rouge s’allume.',
    'setup': 'setup',
    'gear': 'matériel',
    'Studio-ready': 'Prêt studio',
    'Real keys & amps': 'Vrais claviers & amplis',
    'THE LINE-UP': 'LA FORMATION',
    'The players': 'Les musiciens',
    'Two players, one pass.': 'Deux musiciens, une seule passe.',
    'Keys and guitar — tracked separately or together, whichever your song needs.':
        'Claviers et guitare — enregistrés séparément ou ensemble, selon les besoins de votre chanson.',
    'Session keyboard': 'Clavier de session',
    'Piano, Rhodes, synths and organs — played to the arrangement, recorded into your session.':
        'Piano, Rhodes, synthés et orgues — joués sur l’arrangement, enregistrés dans votre session.',
    'Live improvisation': 'Improvisation live',
    'Charts prepared in advance': 'Partitions préparées à l’avance',
    'MIDI + audio take both': 'Prises MIDI + audio',
    'Session guitar': 'Guitare de session',
    'Electric, acoustic and clean amps — parts that sit in the mix and serve the song.':
        'Guitares électriques, acoustiques et amplis propres — des parties qui s’intègrent au mix et servent la chanson.',
    'Original parts': 'Parties originales',
    'Layered takes': 'Prises superposées',
    'DI + amp capture': 'Capture DI + ampli',
    'THE PROCESS': 'LE PROCESSUS',
    'How it works': 'Comment ça marche',
    'Three steps to a played record.': 'Trois étapes vers un disque joué.',
    'We listen': 'Nous écoutons',
    'Send the demo. We listen and prepare the parts and charts.':
        'Envoyez la démo. Nous écoutons et préparons les parties et les partitions.',
    'We play': 'Nous jouons',
    'Live takes over your song, until the feel is exactly right.':
        'Des prises live sur votre chanson, jusqu’à ce que le feeling soit parfait.',
    'We hand it over': 'Nous remettons le tout',
    'Clean session files, ready to mix into your record.':
        'Des fichiers de session propres, prêts à être mixés dans votre disque.',
    'Start a session': 'Lancer une session',
    'Paste a link to the demo or upload details — file links welcome.':
        'Collez un lien vers la démo ou les détails de l’upload — les liens de fichiers sont les bienvenus.',
    'Request the players': 'Demander les musiciens',
    'Good to know': 'Bon à savoir',
    'Sessions run from 2 hours — same day usually possible.':
        'Les sessions démarrent à partir de 2 heures — souvent possible le jour même.',
    'Played in studio or remote, at your place or ours.':
        'Joué en studio ou à distance, chez vous ou chez nous.',
    'You keep every take, DI and capture — no rights hassle.':
        'Vous gardez chaque prise, chaque DI et chaque capture — sans problème de droits.',

    # Book studio page
    'STUDIO TIME': 'TEMPS DE STUDIO',
    'A room tuned for real results.': 'Une salle réglée pour de vrais résultats.',
    'By the hour or the day.': 'À l’heure ou à la journée.',
    'Walk in with a session, walk out with a record-ready mix. Engineer support on hand the whole time.':
        'Entrez avec une session, ressortez avec un mix prêt pour le disque. Un ingénieur disponible en permanence.',
    'tuning': 'réglage',
    'engineer': 'ingénieur',
    'Acoustic-room': 'Salle acoustique',
    'On hand': 'Disponible',
    'RATES': 'TARIFS',
    'Rates': 'Tarifs',
    'Pick your block.': 'Choisissez votre bloc.',
    'Tap a block to jump straight to the availability form.':
        'Cliquez sur un bloc pour accéder directement au formulaire de disponibilité.',
    'FOCUSED': 'CONCENTRÉ',
    'half day': 'demi-journée',
    '4 hours': '4 heures',
    'One focused tracking or mix block.': 'Un bloc d’enregistrement ou de mixage ciblé.',
    'FLEX': 'FLEX',
    'full day': 'journée complète',
    '8 hours': '8 heures',
    'Track the band, then start the mix.': 'Enregistrez le groupe, puis commencez le mix.',
    'session pass': 'passe de session',
    '10 hours': '10 heures',
    'Split across days — use as you go.': 'Répartissez sur plusieurs jours — utilisez-la au fil de l’eau.',
    'CHECK AVAILABILITY': 'VÉRIFIER LES DISPONIBILITÉS',
    'Reserve your slot': 'Réserver votre créneau',
    'Which studio service?': 'Quel service studio ?',
    'Phone number': 'Numéro de téléphone',
    'Preferred time': 'Heure préférée',
    'Additional notes': 'Remarques supplémentaires',
    'Block size, session type, stems — anything that helps us prep the room.':
        'Taille du bloc, type de session, stems — tout ce qui nous aide à préparer la salle.',
    'Request this slot': 'Demander ce créneau',

    # Book a lesson page
    'BOOK A LESSON': 'RÉSERVER UNE LEÇON',
    'Play it for real.': 'Jouez pour de vrai.',
    'Book a lesson': 'Réserver une leçon',
    'At your pace, on studio gear.': 'À votre rythme, sur du matériel de studio.',
    'Private, one-on-one lessons that start where you are — and push you somewhere musical.':
        'Des cours privés, en tête-à-tête, qui commencent là où vous en êtes — et vous emmènent quelque part de musical.',
    'hands-on': 'pratique',
    'level': 'niveau',
    'Real gear': 'Vrai matériel',
    'All levels': 'Tous niveaux',
    'WHAT TO LEARN': 'QUOI APPRENDRE',
    'Subjects': 'Matières',
    'Pick a path.': 'Choisissez un chemin.',
    'Piano & keys': 'Piano & claviers',
    'Chords, voicings and playing that fits songs — from first notes to gig-ready.':
        'Accords, voicings et jeu adapté aux chansons — des premières notes jusqu’aux concerts.',
    'Guitar': 'Guitare',
    'Rhythm, leads and the parts that make a song move. On real amps.':
        'Rythme, leads et les parties qui font bouger une chanson. Sur de vrais amplis.',
    'Audio production': 'Production audio',
    'Recording, editing and mixing your own tracks — in the room it happens in.':
        'Enregistrez, éditez et mixez vos propres morceaux — dans la salle où ça se passe.',
    'Your first lesson': 'Votre première leçon',
    'Instrument, current level and preferred days — we will shape the lesson around it.':
        'Instrument, niveau actuel et jours préférés — nous façonnerons la leçon autour de cela.',
    'Request the lesson': 'Demander la leçon',
    'How lessons work': 'Le déroulement des cours',
    'Private one-on-one — no shared classes.': 'Privé et en tête-à-tête — pas de cours partagés.',
    'Weekly or by the month, at your pace.': 'Hebdomadaire ou mensuel, à votre rythme.',
    'Studio gear provided — just bring your hands.': 'Matériel de studio fourni — apportez simplement vos mains.',
    'See all services': 'Voir tous les services',
    'Pricing': 'Tarifs',
    'Explore all lessons': 'Découvrir tous les cours',

    # Learning page
    'Choose an instrument': 'Choisir un instrument',
    'Build your plan': 'Construire votre plan',
    'Lessons': 'Cours',
    'Pick your instrument.': 'Choisissez votre instrument.',
    'Choose one to start your plan. From your very first session you play real music — instruments and gear provided.':
        'Choisissez-en un pour lancer votre plan. Dès votre toute première séance, vous jouez de la vraie musique — instruments et matériel fournis.',
    'Instruments': 'Instruments',
    'Choose this': 'Choisir celui-ci',
    'Set it up in three steps': 'Réglé en trois étapes',
    'Build your lesson plan.': 'Construisez votre plan de cours.',
    'Choose the instrument, decide how many sessions you want, and pick a private lesson or a group class. The price updates as you go.':
        'Choisissez l’instrument, décidez du nombre de séances, puis optez pour un cours privé ou en groupe. Le prix se met à jour au fur et à mesure.',
    'Sessions': 'Séances',
    'Class type': 'Type de cours',
    'Which instrument?': 'Quel instrument ?',
    'How many sessions?': 'Combien de séances ?',
    'Sessions are once a week — pick a plan that fits your pace.':
        'Les séances ont lieu une fois par semaine — choisissez un plan adapté à votre rythme.',
    'One-on-one or group?': 'Particulier ou en groupe ?',
    'Your plan': 'Votre plan',
    'Not selected': 'Non sélectionné',
    'Length': 'Durée',
    'Price per session': 'Prix par séance',
    'Estimated total': 'Total estimé',
    'Request this plan': 'Envoyer ma demande',
    'Select all three steps to see your total.':
        'Sélectionnez les trois étapes pour voir votre total.',
    'Courses and lessons': 'Cours et leçons',
    'Find your next skill': 'Trouvez votre prochaine compétence',
    'Filter by topic. The list updates to show what’s available in each area.':
        'Filtrez par thème. La liste se met à jour pour montrer ce qui est disponible dans chaque domaine.',
    'Upcoming workshops': 'Ateliers à venir',
    'What students say': 'Ce que disent les élèves',
    'Start with a practical first session': 'Commencez par une première séance pratique',
    'Whether you want to learn an instrument or run the sound for a whole room — the first session is hands-on.':
        'Que vous vouliez apprendre un instrument ou sonoriser toute une salle — la première séance est pratique.',
    'Ask a question': 'Poser une question',

    # Landing — trusted by
    'Trusted by': 'Ils nous font confiance',
    'Trusted by institutions across Canada':
        'Des institutions de confiance partout au Canada',
    'Venues, schools, hospitals and churches across Canada rely on JustTech for sound, systems and training.':
        'Salles, écoles, hôpitaux et églises partout au Canada comptent sur JustTech pour le son, les systèmes et la formation.',
    'Presbyterian Church': 'Église presbytérienne',
    'Pentecost Church': 'Église de Pentecôte',
    'Methodist Church': 'Église méthodiste',
    'Vanguard Hospital': 'Hôpital Vanguard',

    # Landing — capability marquee
    'Sound': 'Son',
    'Streaming': 'Streaming',
    'Video': 'Vidéo',
    'Training': 'Formation',
    'Custom PCs': 'PC sur mesure',
    'Live Events': 'Événements live',
    'Studio Builds': 'Studios sur mesure',

    # About hero — headphones portrait
    'LIVE': 'EN DIRECT',
    'Studio Grade': 'Qualité studio',
    'A creator wearing studio headphones': 'Une créatrice au casque studio, en profil',

    # Landing — our capabilities
    'Our Capabilities': 'Nos compétences',
    'Sound, systems and skills — under one roof.':
        'Le son, les systèmes et les compétences — sous un même toit.',
    'Sound Systems': 'Systèmes audio',
    'Installations designed around the room — church, school, hospital or venue.':
        'Des installations pensées pour chaque pièce — église, école, hôpital ou salle.',
    'Live Sound & Events': 'Son live & événements',
    'Engineers, gear and mixers for services, concerts and conferences.':
        'Ingénieurs du son, matériel et consoles pour cultes, concerts et conférences.',
    'Streaming & Broadcast': 'Streaming & diffusion',
    'Multi-camera live streams and broadcast setups that just work.':
        'Diffusions live multicaméra et systèmes de diffusion à la fois simples et fiables.',
    'Video & Visuals': 'Vidéo & visuel',
    'Production, capture and display for content teams and campuses.':
        'Production, capture et affichage pour les équipes de contenu et les campus.',
    'Custom PCs & Hardware': 'PC sur mesure & matériel',
    'Built-to-spec systems, upgrades and repairs that keep creators creating.':
        'Des systèmes construits sur mesure, des mises à niveau et des réparations qui gardent les créateurs en action.',
    'Training & Mentoring': 'Formation & mentorat',
    'Hands-on sound engineering, streaming and production courses.':
        'Des cours pratiques d’ingénierie du son, de streaming et de production.',
    'See the work': 'Voir le travail',

    # Landing — how we work
    'How we work': 'Comment nous travaillons',
    'From first call to first show — the JustTech way.':
        'Du premier appel à la première représentation — la méthode JustTech.',
    'Consult': 'Consultation',
    'We talk about your space, your budget and the sound you actually want.':
        'Nous parlons de votre espace, de votre budget et du son que vous voulez vraiment.',
    'We plan the system and show you exactly what goes where — before we build.':
        'Nous planifions le système et vous montrons exactement ce qui va où — avant de construire.',
    'Real gear, clean installation, tested and tuned before you go live.':
        'Du vrai matériel, une installation propre, testée et réglée avant le direct.',
    'Train & Support': 'Formation & support',
    'We teach your team to run it and stay on call when you need us.':
        'Nous apprenons à votre équipe à utiliser le système et restons disponibles quand vous avez besoin de nous.',
    'Back to top': 'Revenir en haut',

    # Pricing page
    'Transparent pricing for JustTech services: custom PCs, audio setups, streaming setups, event production, equipment rental, and consultations.':
        'Des tarifs transparents pour les services JustTech : PC sur mesure, configurations audio, systèmes de streaming, production d’événements, location de matériel et consultations.',
    'Honest, upfront pricing for every JustTech service, from custom PCs to full event production.':
        'Des tarifs honnêtes et clairs pour chaque service JustTech, du PC sur mesure à la production d’événements complète.',
    'Pricing introduction': 'Présentation des tarifs',
    'Clear where it can be.': 'Clairs là où c’est possible.',
    'Custom where it needs to be.': 'Sur mesure là où c’est nécessaire.',
    'Every service carries a starting price as a guide. The exact quote is confirmed against the scope and requirements of your project.':
        'Chaque service affiche un prix de départ à titre indicatif. Le devis exact est confirmé selon la portée et les exigences de votre projet.',
    'Service pricing': 'Tarifs par service',
    'Starting prices, by service.': 'Prix de départ, par service.',
    'Each service lists what work typically starts at. Your final quote is confirmed once we know the details of your project.':
        'Chaque service indique le prix auquel démarre habituellement le travail. Votre devis final est confirmé dès que nous connaissons les détails de votre projet.',
    'Contact us for pricing': 'Contactez-nous pour les tarifs',
    'Quotes are prepared against your project scope.':
        'Les devis sont préparés selon la portée de votre projet.',
    'Book this service': 'Réserver ce service',
    'Request a quote': 'Demander un devis',
    'Service pricing is being prepared.': 'Les tarifs des services sont en cours de préparation.',
    'How pricing works': 'Comment fonctionnent les tarifs',
    'Why a quote can vary.': 'Pourquoi un devis peut varier.',
    'Starting prices are a guide. The final figure depends on the specific demands of each project.':
        'Les prix de départ sont une indication. Le montant final dépend des exigences spécifiques de chaque projet.',
    'Scope and size': 'Portée et ampleur',
    'The number of stations, channels or systems involved.':
        'Le nombre de postes, de canaux ou de systèmes concernés.',
    'Venue and location': 'Lieu et emplacement',
    'Logistics, travel and on-site requirements.': 'Logistique, déplacements et exigences sur place.',
    'Equipment and systems': 'Équipement et systèmes',
    'Gear required to reach the standard you need.': 'Le matériel nécessaire pour atteindre le niveau que vous souhaitez.',
    'Duration and complexity': 'Durée et complexité',
    'Timeline, changes and technical difficulty.': 'Calendrier, changements et difficulté technique.',
    'Contact call to action': 'Appel à l’action de contact',
    'Not sure what you need?': 'Vous ne savez pas ce qu’il vous faut ?',
    'Book a consultation.': 'Réservez une consultation.',
    "We'll look at your project and recommend the right scope — with nothing invented along the way.":
        'Nous examinerons votre projet et recommanderons la bonne portée — sans rien inventer au passage.',
    'Book a Consultation': 'Réserver une consultation',

    # Booking page
    'Booking': 'Réservation',
    'Book a consultation or service with JustTech. Choose a service, pick a date, and we will handle the rest.':
        'Réservez une consultation ou un service avec JustTech. Choisissez un service, une date, et nous nous occupons du reste.',
    'Schedule your JustTech consultation or service. Select a service and a date that works for you.':
        'Planifiez votre consultation ou service JustTech. Sélectionnez un service et une date qui vous conviennent.',
    'Booking introduction': 'Présentation de la réservation',
    'Book JustTech': 'Réserver JustTech',
    'Tell us': 'Dites-nous',
    'what you need.': 'ce dont vous avez besoin.',
    'Share the details of your event, setup or project — and we will have the information needed to understand the request.':
        'Partagez les détails de votre événement, de votre installation ou de votre projet — et nous aurons les informations nécessaires pour comprendre la demande.',
    'Booking form': 'Formulaire de réservation',
    'Reserve your slot': 'Réserver votre créneau',
    'Your booking request has been received.': 'Votre demande de réservation a bien été reçue.',
    'Which service do you need?': 'De quel service avez-vous besoin ?',
    'required': 'obligatoire',
    'Company (optional)': 'Entreprise (facultatif)',
    'Preferred date': 'Date préférée',
    'Preferred time': 'Heure préférée',
    'Additional notes': 'Remarques supplémentaires',
    'Tell us about your event, setup or project.': 'Parlez-nous de votre événement, de votre installation ou de votre projet.',
    'Submit request': 'Envoyer la demande',
    'What happens next': 'Et ensuite',
    'Send your request': 'Envoyez votre demande',
    'Fill in the form and submit it.': 'Remplissez le formulaire et envoyez-le.',
    'JustTech reviews the details': 'JustTech examine les détails',
    'Your request is reviewed.': 'Votre demande est examinée.',
    'The next step is discussed with you': 'La prochaine étape est discutée avec vous',
    "We'll be in touch to take it forward.": 'Nous vous recontacterons pour faire avancer les choses.',
    'Prefer to talk?': 'Vous préférez en parler ?',

    # Services page
    'JustTech services: custom-built PCs, audio setups, streaming setups, event production, equipment rental, and one-on-one consultations.':
        'Services JustTech : PC sur mesure, configurations audio, systèmes de streaming, production d’événements, location de matériel et consultations individuelles.',
    'Custom PCs, audio, streaming, and event services — designed, built, and installed by JustTech specialists.':
        'PC sur mesure, audio, streaming et services événementiels — conçus, construits et installés par les spécialistes JustTech.',
    'Introduction': 'Introduction',
    'Technology that works': 'Une technologie qui fonctionne',
    'when it matters.': 'quand ça compte.',
    'Sound systems': 'Systèmes audio',
    'Built for you': 'Conçu pour vous.',
    'Audio setups': 'Configurations audio',
    '4K visual': 'Visuel 4K',
    'JustTech provides audio, streaming, sound systems and custom computing for real-world use — designed, built, tuned and supported by people who stay until it is right.':
        'JustTech fournit des solutions audio, streaming, sonorisation et informatique sur mesure pour un usage réel — conçues, construites, réglées et soutenues par des gens qui restent jusqu’à ce que ce soit juste.',
    'Services overview': 'Aperçu des services',
    'What we do': 'Ce que nous faisons',
    'One team for every A/V need — planned, built and tuned end to end.':
        'Une seule équipe pour chaque besoin A/V — planifié, construit et réglé de bout en bout.',
    'Six services cover the full lifecycle: plan it, build it, run it, support it — and learn to run it yourself.':
        'Six services couvrent l’ensemble du cycle : planifier, construire, faire tourner, soutenir — et apprendre à gérer soi-même.',
    'Services index': 'Index des services',
    'Service details': 'Détails des services',
    'Audio mixing console during a setup': 'Console de mixage audio lors d’une installation',
    'Live concert audience under stage lights during a performance':
        'Public d’un concert live sous les lumières de scène pendant une représentation',
    'Event audio': 'Audio événementiel',
    'You focus on the event.': 'Vous vous concentrez sur l’événement.',
    'We handle the sound.': 'Nous gérons le son.',
    'From a church service to a full concert stage, JustTech can plan, set up, operate and support the sound for the entire event. We arrive early, soundcheck properly and stay until the last note.':
        'D’un service religieux à une scène de concert complète, JustTech peut planifier, installer, opérer et soutenir le son pour l’ensemble de l’événement. Nous arrivons tôt, faisons le soundcheck correctement et restons jusqu’à la dernière note.',
    'Events we support': 'Événements que nous soutenons',
    'Concerts': 'Concerts',
    'Church services': 'Cultes religieux',
    'Conferences': 'Conférences',
    'Corporate events': 'Événements d’entreprise',
    'Private events & live performances': 'Événements privés & représentations en direct',
    'What JustTech handles': 'Ce que JustTech prend en charge',
    'Setup and soundcheck': 'Installation et soundcheck',
    'Mixing and monitoring': 'Mixage et monitoring',
    'Live operation on the day': 'Exploitation en direct le jour J',
    'Technical support and troubleshooting': 'Support technique et dépannage',
    'Including:': 'Incluant :',
    'Book this': 'Réserver',

    # Event audio — featured gallery card fact lines
    'Live stage · FOH · Monitors': 'Scène live · FOH · Monitors',
    'Clear speech · Hymns · Weekly': 'Parole claire · Hymnes · Hebdo',
    'Keynotes · Panels · Q&A': 'Keynotes · Panels · Q&A',
    'Launches · Dinners · Gala': 'Lancements · Dîners · Gala',
    'Weddings · Showcases · Private': 'Mariages · Showcases · Privé',
    'Early arrival · Room tuning': 'Arrivée anticipée · Réglage de la salle',
    'FOH · Monitors · Clarity': 'FOH · Monitors · Clarté',
    'Engineers on deck · Live desk': 'Ingénieurs en poste · Console live',
    'On-site fixes · Standby': 'Dépannage sur place · Standby',

    'Streaming & production': 'Streaming & production',
    'Streaming you can rely on, live.': 'Un streaming fiable, en direct.',
    'We design and configure streaming and production systems that hold up on air — cameras, capture, audio into the stream, encoding and monitoring. Then we test it, rehearse it and stay on standby while you are live.':
        'Nous concevons et configurons des systèmes de streaming et de production qui tiennent bon à l’antenne — caméras, capture, audio dans le flux, encodage et monitoring. Ensuite nous testons, répétons et restons en veille pendant votre direct.',
    'What you get is a clean, stable stream and a setup your own team can operate — not a mystery rig that needs emergency support every time you go live.':
        'Ce que vous obtenez, c’est un flux propre et stable et une installation que votre propre équipe peut opérer — pas une mystérieuse machine qui nécessite un dépannage d’urgence à chaque diffusion.',
    'Streaming studio setup with camera and lighting': 'Configuration de studio de streaming avec caméra et éclairage',
    'Who JustTech is built for': 'Pour qui JustTech est fait',
    "Who it's for": 'Pour qui c’est fait',
    'Built for the people who use it': 'Conçu pour ceux qui l’utilisent',
    'JustTech works wherever sound and picture have to be dependable — for the room, the event, the stream and the desk.':
        'JustTech travaille partout où le son et l’image doivent être fiables — pour la salle, l’événement, le streaming et le bureau.',
    'The room': 'La salle',
    'Churches, schools, auditoriums and venues that need dependable sound, week after week.':
        'Églises, écoles, auditoriums et lieux qui ont besoin d’un son fiable, semaine après semaine.',
    'The event': 'L’événement',
    'Concerts, conferences, corporate and private events that need sound and support on the day.':
        'Concerts, conférences, événements d’entreprise et privés qui ont besoin de son et de support le jour J.',
    'The stream': 'Le streaming',
    'Creators, channels and businesses producing regular live content that needs to look and sound right.':
        'Créateurs, chaînes et entreprises produisant du contenu live régulier qui doit bien paraître et bien sonner.',
    'The desk': 'Le bureau',
    'Editors, producers, musicians and streamers who need a computer that keeps up with the work.':
        'Éditeurs, producteurs, musiciens et streamers qui ont besoin d’un ordinateur qui suit le rythme du travail.',
    'How a project works': 'Comment se déroule un projet',
    'From first call to final soundcheck.': 'Du premier appel au dernier soundcheck.',
    'A simple process that keeps you in the loop at every stage — whether it is an event, an installation, a stream or a build.':
        'Un processus simple qui vous tient au courant à chaque étape — que ce soit un événement, une installation, un streaming ou un montage.',
    'Project process': 'Déroulement du projet',
    'Tell us what you need': 'Dites-nous ce dont vous avez besoin',
    'A short call about your space, event or setup. We ask the right questions.':
        'Un appel rapide à propos de votre espace, de votre événement ou de votre installation. Nous posons les bonnes questions.',
    'We assess the requirement': 'Nous évaluons le besoin',
    'We check the space, the load, the budget and the people who will run it.':
        'Nous vérifions l’espace, la charge, le budget et les personnes qui l’exploiteront.',
    'We design the right setup': 'Nous concevons la bonne installation',
    'A clear plan and an honest quote — no vague lists, no surprises.':
        'Un plan clair et un devis honnête — pas de listes vagues, pas de surprises.',
    'We build, configure or install': 'Nous construisons, configurons ou installons',
    'Installation, configuration and tuning until it sounds and behaves right.':
        'Installation, configuration et réglage jusqu’à ce que le son et le comportement soient parfaits.',
    'We test and support': 'Nous testons et soutenons',
    'Soundcheck, run-through and practical support long after the job is done.':
        'Soundcheck, répétition et support pratique longtemps après la fin du travail.',
    'Get started': 'Commencer',

    # Portfolio page
    'Portfolio': 'Portfolio',
    'Recent JustTech work: custom PCs, audio setups, streaming rigs, and event production — designed and built end to end.':
        'Travaux récents de JustTech : PC sur mesure, configurations audio, rigs de streaming et production d’événements — conçus et construits de bout en bout.',
    'Selected projects from JustTech, showing the systems we design, build, and install.':
        'Projets sélectionnés de JustTech, présentant les systèmes que nous concevons, construisons et installons.',
    'Portfolio introduction': 'Présentation du portfolio',
    'Built for real spaces, real events': 'Conçu pour de vrais espaces, de vrais événements',
    'and real workflows.': 'et de vrais flux de travail.',
    'Audio systems, events, streaming setups and custom builds — designed around how they actually need to work.':
        'Systèmes audio, événements, configurations de streaming et montages sur mesure — conçus autour de la façon dont ils doivent réellement fonctionner.',
    'Selected work': 'Travaux sélectionnés',
    'Work coming soon': 'Travaux à venir',
    'Project work will appear here as it is added.':
        'Les projets apparaîtront ici au fur et à mesure de leur ajout.',
    'In the meantime, tell us what you are planning — or explore what JustTech can do.':
        'En attendant, dites-nous ce que vous planifiez — ou découvrez ce que JustTech peut faire.',
    'Working on something similar?': 'Vous travaillez sur quelque chose de similaire ?',
    "Tell us what you're planning.": 'Dites-nous ce que vous planifiez.',
    "Whether it's an event, a build or a stream — we'll figure out what it needs.":
        'Qu’il s’agisse d’un événement, d’un montage ou d’un streaming — nous déterminerons ce dont il a besoin.',

    # Success + workshop components
    'Thanks — your message has been received.': 'Merci — votre message a bien été reçu.',
    'JustTech will review your message and follow up with you.':
        'JustTech examinera votre message et vous recontactera.',
    'Return home': 'Revenir à l’accueil',
    'Booking request received': 'Demande de réservation reçue',
    'Your booking request has been received. JustTech will review the details and the next step will be discussed with you.':
        'Votre demande de réservation a bien été reçue. JustTech examinera les détails et la prochaine étape sera discutée avec vous.',
    'Register for': 'S’inscrire à',
    'Confirm Registration': 'Confirmer l’inscription',
    'Cancel': 'Annuler',
    'Registered!': 'Inscrit !',
    "You're signed up for": 'Vous êtes inscrit pour',
    "We'll send confirmation to your email.": 'Nous enverrons une confirmation à votre e-mail.',
    'lessons available.': 'leçons disponibles.',
    'lesson available.': 'leçon disponible.',
    'No lessons added yet.': 'Aucune leçon ajoutée pour l’instant.',
    "What you'll learn": 'Ce que vous allez apprendre',
    'New lessons and workshops will appear here when available.':
        'De nouvelles leçons et de nouveaux ateliers apparaîtront ici dès qu’ils seront disponibles.',

    # Shared / global UI strings
    'FAQ': 'FAQ',
    "Let's talk about": 'Parlons de',
    'what you need.': 'ce dont vous avez besoin.',
    'Email': 'E-mail',
    'Tell us about your project or question.':
        'Parlez-nous de votre projet ou de votre question.',
    'Loading': 'Chargement',
    'Initializing': 'Initialisation',
    'Skip to content': 'Aller au contenu',
    'Sound. Systems. Skills.': 'Son. Systèmes. Compétences.',

    # Learning page
    'Learn an instrument': 'Apprenez un instrument',
    'your way.': 'à votre façon.',
    'Organ, piano, guitar or drums — pick what you want to play, choose how many sessions you will take, and decide: private or in a group.':
        'Orgue, piano, guitare ou batterie — choisissez ce que vous voulez jouer, décidez du nombre de séances, et optez : en privé ou en groupe.',
    'All': 'Tous',

    # About page — ethos / journey (gap fill)
    'Just Tech is a team of technicians, builders and teachers who believe great audio starts with great people. Founded in 2018, we design, build and teach — side by side with our clients.':
        'Just Tech est une équipe de techniciens, de constructeurs et de pédagogues convaincus qu’un grand son commence par de grandes personnes. Fondée en 2018, nous concevons, construisons et formons — aux côtés de nos clients.',
    'Spinning JustTech studio vinyl record': 'Vinyle du studio JustTech en rotation',
    'Mission and values': 'Mission et valeurs',
    'Our Ethos': 'Notre philosophie',
    'Mission & Values': 'Mission & valeurs',
    'Why we build, mix and teach the way we do.':
        'Pourquoi nous construisons, mixons et formons comme nous le faisons.',
    'Our Mission': 'Notre mission',
    'Great sound, made simple.': 'Un grand son, simplifié.',
    'To make professional audio and visual technology approachable — wiring good gear, honest builds and hands-on teaching into every project until it works for the people using it.':
        'Rendre la technologie audio et visuelle professionnelle accessible — du bon matériel, des installations honnêtes et une formation pratique dans chaque projet, jusqu’à ce que cela fonctionne pour ceux qui l’utilisent.',
    'Our Vision': 'Notre vision',
    'Every space sounds confident.': 'Chaque espace sonne avec assurance.',
    'A world where every church, school, stage and home studio speaks with clarity — powered by equipment people understand and skills they can keep.':
        'Un monde où chaque église, école, scène et studio domestique parle avec clarté — grâce à un équipement que l’on comprend et des compétences que l’on garde.',
    'Sound first': 'Le son d’abord',
    'Every decision is judged by how it sounds in the real room — not on paper.':
        'Chaque décision se juge au son dans la vraie salle — pas sur le papier.',
    'Teach as we build': 'Former en construisant',
    'We explain what we install. Understanding is part of the deliverable.':
        'Nous expliquons ce que nous installons. La compréhension fait partie de la livraison.',
    'Honest gear': 'Un matériel honnête',
    'We recommend what fits the budget and the job — no jargon, no upselling.':
        'Nous recommandons ce qui correspond au budget et au travail — pas de jargon, pas de vente forcée.',
    'Stay to the end': 'Rester jusqu’au bout',
    'If the mix is not working, we are not done. We live with the outcome, not just the delivery.':
        'Si le mix ne fonctionne pas, nous n’avons pas terminé. Nous vivons avec le résultat, pas seulement avec la livraison.',
    'Our Journey': 'Notre parcours',
    'Milestones.': 'Jalons.',
    'From one mixing desk to a full studio — the moments that built Just Tech.':
        'D’une table de mixage à un studio complet — les moments qui ont construit Just Tech.',
    'Selected work.': 'Travaux sélectionnés.',
    'Rooms, stages and studios we have wired and built — and the people behind them.':
        'Salles, scènes et studios que nous avons câblés et construits — et les personnes derrière eux.',
    'Selected projects appear here once featured in the admin panel.':
        'Les projets sélectionnés apparaîtront ici une fois mis en avant dans le panneau d’administration.',

    # Studio + band session pages (gap fill)
    'Track, mix and master by the hour or by the day — with the gear and the room to back it up.':
        'Enregistrez, mixez et masterisez à l’heure ou à la journée — avec le matériel et la salle pour le faire.',
    'Half day': 'Demi-journée',
    'Full day': 'Journée complète',
    'Session': 'Session',
    'Session keyboards and guitar for the song you are about to produce — played, recorded and honed in your studio.':
        'Claviers et guitare de session pour la chanson que vous vous apprêtez à produire — joués, enregistrés et affinés dans votre studio.',

    # Share / contact widgets
    'NOW TRACKING': 'EN COURS D’ENREGISTREMENT',
    'Contact us': 'Nous contacter',

    # Learning page — filters / instructors (gap fill)
    'Instrument': 'Instrument',
    'Courses': 'Cours',
    'Filter lessons by category': 'Filtrer les leçons par catégorie',
    'Workshops': 'Ateliers',
    'Register straight from this page — no extra forms, no waiting.':
        'Inscrivez-vous directement depuis cette page — pas de formulaires supplémentaires, pas d’attente.',
    'Instructors': 'Instructeurs',
    'Learn from people who do it daily': 'Apprenez auprès de gens qui le font tous les jours',
    'Every instructor is an active engineer, musician or producer — not a full-time lecturer.':
        'Chaque instructeur est un ingénieur, un musicien ou un producteur en activité — pas un professeur à temps plein.',

    # Services / get-started CTAs
    'Tell us about the room, the event, the stream or the build — we will take it from there.':
        'Parlez-nous de la salle, de l’événement, du streaming ou du montage — nous prendrons les choses d’ici.',
    'Send JustTech a message — sessions, installs, builds or anything that does not fit a box.':
        'Envoyez un message à JustTech — séances, installations, montages ou tout ce qui ne rentre pas dans une case.',

    # Locator (map) component
    'JustTech — based in Barrie, Ontario, Canada': 'JustTech — basé à Barrie, Ontario, Canada',
    'Play the location sequence by scrolling': 'Jouer la séquence de localisation en faisant défiler',
    'Scroll': 'Faire défiler',
    'JustTech is based in Barrie, Ontario, Canada — 44.3894° North, 79.6900° West.':
        'JustTech est basé à Barrie, Ontario, Canada — 44,3894° Nord, 79,6900° Ouest.',

    # Services — event audio marquee lanes
    'Events': 'Événements',
    'Concert crowd under stage lights': 'Public de concert sous les lumières de scène',
    'Sunlit church interior': 'Intérieur d’église baigné de lumière',
    'Conference speaker on stage': 'Conférencier sur scène',
    'Corporate event gathering': 'Réception événementielle d’entreprise',
    'Live performance confetti crowd': 'Public sous les confettis d’un concert',
    'Full shows — FOH mixing, monitoring and support until the encore.':
        'Des concerts complets — mixage FOH, monitoring et support jusqu’au rappel.',
    'Dependable, clear sound for worship — week after week.':
        'Un son clair et fiable pour le culte — semaine après semaine.',
    'Speech-first sound for agendas, keynotes and Q&A.':
        'Un son orienté parole pour les ordres du jour, les discours et les questions.',
    'Launch events, dinners and announcements — handled seamlessly.':
        'Lancements, dîners et annonces — gérés sans accroc.',
    'Weddings and showcases — sound that fits the moment.':
        'Mariages et showcases — un son qui s’adapte au moment.',
    'We arrive early and tune the room before anyone walks in.':
        'Nous arrivons tôt et réglons la salle avant l’arrivée de quiconque.',
    'Clean FOH and monitor mixes, dialed to the room.':
        'Des mixages FOH et monitoring nets, réglés pour la salle.',
    'Our engineers run the show so your team can host it.':
        'Nos ingénieurs font tourner le spectacle pour que votre équipe puisse l’accueillir.',
    'Fast fixes on site — and standby when you need it.':
        'Dépannage rapide sur place — et disponibilité quand vous en avez besoin.',
}