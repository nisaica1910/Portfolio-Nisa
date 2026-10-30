from flask import Flask, render_template, request
import re

from flask import Flask, render_template, request
from markupsafe import Markup, escape

app = Flask(__name__)

# ======================================================
#  Semua konten portfolio diatur dari sini.
#  Teks yang beda antar bahasa ditulis sebagai
#  {"id": "...", "en": "..."} — field lain (tags, nama
#  file gambar, link) cukup string biasa, nggak perlu
#  diterjemahkan.
# ======================================================

UI_STRINGS = {
    "nav_home": {"id": "Home", "en": "Home"},
    "nav_about": {"id": "Tentang", "en": "About"},
    "nav_experience": {"id": "Pengalaman", "en": "Experience"},
    "nav_organizations": {"id": "Organisasi", "en": "Organizations"},
    "nav_projects": {"id": "Project", "en": "Projects"},
    "nav_certificates": {"id": "Sertifikat", "en": "Certificates"},
    "hero_greeting": {"id": "Hai, saya", "en": "Hi, I'm"},
    "hero_view_projects": {"id": "Lihat Project", "en": "View Projects"},
    "hero_download_cv": {"id": "Download CV", "en": "Download CV"},
    "about_eyebrow": {"id": "Tentang Saya", "en": "About Me"},
    "about_title": {"id": "Profil Singkat", "en": "Quick Profile"},
    "experience_eyebrow": {"id": "Perjalanan", "en": "Journey"},
    "experience_title": {"id": "Pengalaman", "en": "Experience"},
    "view_content": {"id": "Lihat Portofolio Konten", "en": "View Content Portfolio"},
    "content_title": {"id": "Portofolio Konten", "en": "Content Portfolio"},
    "content_intro": {"id": "Beberapa konten pilihan yang aku kerjakan untuk Biro Karir. Klik kartu untuk menontonnya.", "en": "A selection of content I worked on for the Career Bureau. Click a card to watch it."},
    "content_my_role": {"id": "Peranku", "en": "My role"},
    "content_watch": {"id": "Tonton", "en": "Watch"},
    "content_view_ig": {"id": "Lihat Akun Instagram", "en": "View Instagram Account"},
    "content_featured": {"id": "Tayang di acara wisuda UMB", "en": "Shown at the UMB graduation ceremony"},
    "organizations_eyebrow": {"id": "Keterlibatan", "en": "Involvement"},
    "organizations_title": {"id": "Organisasi & Event", "en": "Organizations & Events"},
    "organizations_sub": {"id": "Organisasi", "en": "Organizations"},
    "events_sub": {"id": "Event", "en": "Events"},
    "projects_eyebrow": {"id": "Karya", "en": "Work"},
    "projects_title": {"id": "Project", "en": "Projects"},
    "view_detail": {"id": "Lihat Detail", "en": "View Details"},
    "open_project": {"id": "Buka Demo", "en": "Open Demo"},
    "project_purpose": {"id": "Dibangun untuk", "en": "Built for"},
    "project_partner": {"id": "Mitra / Perusahaan", "en": "Partner / Company"},
    "project_features": {"id": "Fitur Utama", "en": "Key Features"},
    "project_tech": {"id": "Teknologi", "en": "Tech Stack"},
    "view_github": {"id": "Lihat di GitHub", "en": "View on GitHub"},
    "certificates_eyebrow": {"id": "Pencapaian", "en": "Achievements"},
    "certificates_title": {"id": "Sertifikat", "en": "Certificates"},
    "view_photo": {"id": "Lihat foto", "en": "View photo"},
    "skills_tab_hard": {"id": "Hard Skills", "en": "Hard Skills"},
    "skills_tab_soft": {"id": "Soft Skills", "en": "Soft Skills"},
    "skills_tab_lang": {"id": "Bahasa", "en": "Languages"},
    "skills_desc_hard": {"id": "Teknologi & tools yang aku pakai", "en": "Technologies & tools I work with"},
    "skills_desc_soft": {"id": "Cara aku bekerja bersama orang lain", "en": "How I work with other people"},
    "skills_desc_lang": {"id": "Bahasa yang aku kuasai", "en": "Languages I speak"},
    "view_certificate": {"id": "Lihat Sertifikat", "en": "View Certificate"},
    "show_more": {"id": "Lihat Semua", "en": "View All"},
    "show_less": {"id": "Tampilkan Lebih Sedikit", "en": "Show Less"},
}

PROFILE = {
    "name": "Khairunnisa Ramadhan",
    "nickname": {"id": "Portofolio", "en": "Portfolio"},
    "role": "Fresh Graduate — Informatics Engineering",
    "tagline": {
        "id": "Lulusan Teknik Informatika yang memiliki minat pada pengembangan web, analisis data, dan solusi digital. Senang memecahkan masalah, mengeksplorasi teknologi baru, serta membangun aplikasi yang bermanfaat.",
        "en": "A versatile IT graduate with interests in web development, data analysis, and digital solutions. Passionate about solving problems, exploring new technologies, and building useful applications.",
    },
"about_0": { "id": ( "Saya merupakan lulusan Teknik Informatika Universitas Mercu Buana " "dengan IPK 3.85/4.00. Saya memiliki ketertarikan pada bidang " "teknologi informasi, pengembangan web, dan analisis data. Saya " "senang mempelajari hal baru serta mengembangkan kemampuan untuk " "menghasilkan solusi yang sesuai dengan kebutuhan pengguna." ), "en": ( "I am an Informatics Engineering graduate from Universitas Mercu " "Buana with a GPA of 3.85/4.00. I am interested in information " "technology, web development, and data analysis. I enjoy learning " "new things and developing my skills to create solutions that " "meet users' needs." ), }, "about_1": { "id": ( "Saya memiliki pengalaman di bidang pengembangan aplikasi web, " "pengelolaan database, analisis data, serta administrasi. Melalui " "pengalaman profesional, magang, organisasi, dan proyek, saya " "terbiasa bekerja secara kolaboratif, mengelola tugas, menganalisis " "permasalahan, serta menyelesaikan pekerjaan secara terstruktur. " "Saya juga memiliki pengalaman berkoordinasi dalam tim dan " "beradaptasi dengan lingkungan kerja yang berbeda." ), "en": ( "I have experience in web application development, database " "management, data analysis, and administration. Through professional " "experience, internships, organizational activities, and projects, " "I have developed the ability to collaborate with others, manage " "tasks, analyze problems, and work in an organized manner. I am " "also experienced in team coordination and adapting to different " "working environments." ), }, "about_2": { "id": ( "Saya adalah pribadi yang teliti, adaptif, bertanggung jawab, " "dan memiliki semangat belajar yang tinggi. Saya terbuka terhadap " "berbagai peluang untuk mengembangkan kemampuan, memperluas " "pengalaman profesional, serta memberikan kontribusi positif bagi " "tim dan perusahaan. Saya percaya bahwa kemauan untuk terus belajar " "dan kemampuan bekerja sama merupakan bagian penting dalam " "menghasilkan pekerjaan yang berkualitas." ), "en": ( "I am detail-oriented, adaptable, responsible, and eager to learn. " "I am open to various opportunities to develop my skills, expand " "my professional experience, and make positive contributions to " "a team and organization. I believe that continuous learning and " "collaboration are essential to delivering quality work." ),
    },
    "photo": "profile.jpg",
    "photo_secondary": "profile-2.jpg",  # foto kedua buat kolase di section About
    "email": "khairunnisaramadhan547@gmail.com",
    "github": "https://github.com/nisaica1910",
    "linkedin": "https://www.linkedin.com/in/khairunnisa-ramadhan/",
    "cv_link": "https://drive.google.com/file/d/1KSMbXZY-GPC6BfX87b_sEsZIGlSbT1uR/view?usp=sharing",
    "stats": [
        {"value": "3.85/4.0", "label": {"id": "GPA", "en": "GPA"}},
        {"value": "5+", "label": {"id": "Pengalaman Kerja", "en": "Work Experience"}},
    ],
}

PILLARS = [
    {
        "icon": "🧩",
        "title": "Fullstack Web Development",
        "text": {
            "id": "Membangun aplikasi web dari frontend sampai backend memakai React.js/Next.js, Laravel, Python, dan MySQL.",
            "en": "Building web applications from frontend to backend using React.js/Next.js, Laravel, Python, and MySQL.",
        },
    },
    {
        "icon": "🧠",
        "title": "Machine Learning & NLP",
        "text": {
            "id": "Membangun model klasifikasi teks dan chatbot NLP berbasis AWS, dari preprocessing data sampai evaluasi performa model.",
            "en": "Building text classification models and AWS-based NLP chatbots, from data preprocessing to model performance evaluation.",
        },
    },
    {
        "icon": "🗂️",
        "title": "Data & Database Administration",
        "text": {
            "id": "Terbiasa mengelola, memverifikasi, dan menganalisis data — dari review database institusi sampai pelaporan hasil survei.",
            "en": "Experienced in managing, verifying, and analyzing data — from institutional database reviews to survey reporting.",
        },
    },
]

SKILLS = {
    "hard": [
        "Python", "PHP", "C++", "HTML", "Laravel", "React.js", "Next.js",
        "MySQL", "RapidMiner", "AWS", "Microsoft Excel", "Word", "PowerPoint", "Canva",
    ],
    "soft": {
        "id": ["Komunikasi & Kolaborasi", "Manajemen Waktu", "Kerja Tim", "Pemecahan Masalah", "Keterampilan Organisasi", "Kepemimpinan"],
        "en": ["Communication & Collaboration", "Time Management", "Teamwork", "Problem Solving", "Organizational Skills", "Leadership"],
    },
    "languages": {
        "id": ["Bahasa Indonesia", "Bahasa Inggris"],
        "en": ["Indonesian", "English"],
    },
}

ROLE_LABELS = {
    "talent": {"id": "Talent", "en": "Talent"},
    "concept": {"id": "Konsep Video", "en": "Video Concept"},
    "script": {"id": "Script Writer", "en": "Scriptwriter"},
    "editor": {"id": "Editor", "en": "Editor"},
    "director": {"id": "Pengarah Video", "en": "Video Director"},
    "shooting": {"id": "Pengambilan Video", "en": "Videographer"},
}

EXPERIENCES = [
    {
            "role": "Surveyor Data Analyst",
            "org": "Biro Karir, Hubungan dan Penelusuran Alumni — Universitas Mercu Buana",
            "logo": "logo-umb.jpg",
            "period": {"id": "Nov 2025 — Apr 2026", "en": "Nov 2025 — Apr 2026"},
            "tagline": {
                "id": "Mengubah respons survei menjadi data alumni yang andal.",
                "en": "Turning survey responses into reliable alumni data.",
            },
            "points": {
                "id": [
                    "Mengumpulkan data **tracer study alumni** melalui **survei terstruktur** untuk laporan pelacakan alumni universitas.",
                    "**Memverifikasi, membersihkan, dan merapikan** data survei agar tetap **lengkap dan akurat**.",
                    "**Menganalisis data ketenagakerjaan alumni**, merangkum temuan untuk pelaporan institusi, dan berkoordinasi dengan responden untuk meningkatkan **tingkat respons**.",
                ],
                "en": [
                    "Collected **alumni tracer study** data through **structured surveys** for the university's alumni tracking reports.",
                    "**Verified, cleaned, and organized** survey data to keep it **complete and accurate**.",
                    "**Analyzed alumni employment data**, summarized findings for institutional reporting, and coordinated with respondents to improve **response rates**.",
                ],
            },
            "tags": ["Data Analysis", "Microsoft Excel", "Survey"],
        },
        {
        "role": "Content Creator",
        "org": "Biro Karir, Hubungan dan Penelusuran Alumni — Universitas Mercu Buana",
        "logo": "logo-umb.jpg",  # samakan dengan logo di kartu Surveyor Data Analyst
        "period": {"id": "Sep 2025 — Sep 2026", "en": "Sep 2025 — Sep 2026"},
        "tagline": {
            "id": "Dari ide dan script sampai tayang, satu konten dikerjakan dari awal sampai akhir.",
            "en": "From idea and script to publish, owning each piece of content end to end.",
        },
        "points": {
            "id": [
                "Membuat **konten video dan reels** untuk Biro Karir, mulai dari **konsep, penulisan script, pengambilan video, hingga editing** memakai **Canva** dan **CapCut**.",
                "Berperan sebagai **talent**, **script writer**, **editor**, dan **pengarah video** di berbagai konten, termasuk satu video yang **ditayangkan di acara wisuda Universitas Mercu Buana**.",
                "Menulis **caption** dan membuat **live report** kegiatan Biro Karir untuk publikasi di Instagram.",
            ],
            "en": [
                "Produced **video and reels content** for the Career Bureau, from **concept, scriptwriting, and filming to editing** using **Canva** and **CapCut**.",
                "Took on roles as **talent**, **scriptwriter**, **editor**, and **video director** across different pieces, including a video **shown at the Universitas Mercu Buana graduation ceremony**.",
                "Wrote **captions** and produced **live reports** of Career Bureau activities for Instagram.",
            ],
        },
        "tags": ["Content Creation", "Video Editing", "Scriptwriting", "Canva", "CapCut"],
        "content": {
            "instagram": "https://www.instagram.com/kariralumni.umb/",
            "entries": [
                {"platform": "youtube", "url": "https://youtu.be/J2JBFbqfzrU", "youtube_id": "J2JBFbqfzrU",
                 "thumb": "img/youtube-cover.jpg",
                 "title": {"id": "Video untuk Acara Wisuda UMB", "en": "Video for the UMB Graduation Ceremony"},
                 "featured": True, "roles": ["talent", "concept", "script", "editor"]},
                {"platform": "instagram", "url": "https://www.instagram.com/reel/DbKJGlip2tX/", "thumb": "img/reel-1.jpg", "roles": ["script", "director"]},
                {"platform": "instagram", "url": "https://www.instagram.com/reel/DbC06EcJTS3/", "thumb": "img/reel-2.jpg", "roles": ["talent", "concept"]},
                {"platform": "instagram", "url": "https://www.instagram.com/reel/DYYq-4pp01x/", "thumb": "img/reel-3.jpg", "roles": ["editor", "concept"]},
                {"platform": "instagram", "url": "https://www.instagram.com/reel/DYYZIGCpCsp/", "thumb": "img/reel-4.jpg", "roles": ["shooting", "editor", "concept"]},
                {"platform": "instagram", "url": "https://www.instagram.com/reel/DXqHLeOiT3j/", "thumb": "img/reel-5.jpg", "roles": ["talent", "script", "editor"]},
                {"platform": "instagram", "url": "https://www.instagram.com/reel/DW5LezdCZb9/", "thumb": "img/reel-6.jpg", "roles": ["talent", "script", "editor"]},
                {"platform": "instagram", "url": "https://www.instagram.com/reel/DWnlq-0CY9g/", "thumb": "img/reel-7.jpg", "roles": ["concept", "editor"]},
            ],
        },
    },
    {
        "role": "Fullstack Developer",
        "org": "PT. Winnicode Garuda Teknologi — Work From Home, Yogyakarta",
        "logo": "logo-winnicode.jpeg",
        "period": {"id": "Feb 2025 — Mei 2025", "en": "Feb 2025 — May 2025"},
        "tagline": {
            "id": "Dari kebutuhan HR sampai dashboard real-time.",
            "en": "From HR needs to a real-time dashboard.",
        },
        "points": {
            "id": [
                "Mengembangkan **sistem absensi digital berbasis web** untuk perusahaan dengan skema kerja **hybrid/remote** di industri media digital.",
                "Membangun frontend dengan **React.js/Next.js** dan backend **Laravel** + **MySQL** untuk pencatatan kehadiran **real-time**.",
                "Merancang fitur **izin/cuti online**, **dashboard HR real-time**, dan **laporan analitik kehadiran**, serta menyusun **proposal proyek** (kebutuhan sistem, scope, tech stack, timeline).",
            ],
            "en": [
                "Developed a **web-based digital attendance system** for companies with **hybrid/remote** work arrangements in the digital media industry.",
                "Built the frontend with **React.js/Next.js** and the backend with **Laravel** + **MySQL** for **real-time** attendance tracking.",
                "Designed **online leave requests**, a **real-time HR dashboard**, and **attendance analytics reporting**, and authored the **project proposal** (requirements, scope, tech stack, timeline).",
            ],
        },
        "tags": ["React.js", "Next.js", "Laravel", "MySQL"],
    },
       {
            "role": "Database Administrator Intern",
            "org": "Data and Information Center, Ministry of Energy and Mineral Resources",
            "logo": "logo-esdm.png",
            "period": {"id": "Feb 2025 — Mar 2025", "en": "Feb 2025 — Mar 2025"},
            "tagline": {
                "id": "Memastikan database aplikasi memenuhi standar.",
                "en": "Making sure application databases meet the standard.",
            },
            "points": {
                "id": [
                    "Membantu tim IT **meninjau database aplikasi** yang diajukan oleh unit-unit di Kementerian.",
                    "**Memverifikasi kelengkapan dokumen** dan **kepatuhan terhadap standar database**.",
                    "Merapikan informasi database untuk proses evaluasi dan **mendokumentasikan temuan review** untuk tim IT.",
                ],
                "en": [
                    "Assisted the IT team in **reviewing application databases** submitted by units within the Ministry.",
                    "**Verified document completeness** and **compliance with database standards**.",
                    "Organized database information for the evaluation process and **documented review findings** for the IT team.",
                ],
            },
            "tags": ["Database", "MySQL", "Documentation"],
        },
    {
        "role": "Project Leader",
        "org": "RevoU — Cloud and Gen AI Machine Learning Program",
        "logo": "logo-revou.jpeg",
        "period": {"id": "Sep 2024 — Des 2024", "en": "Sep 2024 — Dec 2024"},
        "tagline": {
            "id": "Memimpin tim membangun chatbot AWS hingga masuk Top 2.",
            "en": "Leading a team to build an AWS chatbot all the way to Top 2.",
        },
        "points": {
            "id": [
                "Memimpin tim merancang, membangun, dan mengimplementasikan **MEMORA**, chatbot berbasis **AWS** dengan respons efisien dan cerdas.",
                "Mengoordinasikan **perencanaan proyek, pembagian tugas, dan milestone** pengembangan.",
                "Diakui sebagai salah satu **Top 2 Best Teams** atas pendekatan inovatif dan implementasi yang berhasil.",
            ],
            "en": [
                "Led a team in designing, building, and implementing **MEMORA**, an **AWS**-based chatbot delivering efficient and intelligent responses.",
                "Coordinated **project planning, task distribution, and development milestones**.",
                "Recognized as one of the **Top 2 Best Teams** for an innovative approach and successful implementation.",
            ],
        },
        "tags": ["AWS", "Machine Learning", "Leadership"],
    },
{
        "role": "System Developer (Remote)",
        "org": "MI At-Taubah — SIDOEL Project",
        "logo": "logo-attaubah.jpeg",
        "period": {"id": "Des 2023 — Jan 2025", "en": "Dec 2023 — Jan 2025"},
        "tagline": {
            "id": "Mendigitalkan data sekolah dalam satu website terpadu.",
            "en": "Digitalizing school data in one integrated website.",
        },
        "points": {
            "id": [
                "Berkolaborasi dengan tim IT MI At-Taubah membangun **SIDOEL**, website terintegrasi untuk **data institusi**.",
                "Mencakup **data siswa, data guru, dan administrasi sekolah** dalam satu sistem.",
            ],
            "en": [
                "Collaborated with MI At-Taubah's IT team to build **SIDOEL**, an integrated website for **institutional data**.",
                "Covers **student records, teacher records, and school administration** in a single system.",
            ],
        },
        "tags": ["Web Development", "PHP"],
    },
        {
        "role": "Management Intern",
        "org": "PT APLUS PACIFIC",
        "logo": "logo-aplus.png",
        "period": {"id": "Apr 2024 — Mei 2024", "en": "Apr 2024 — May 2024"},
        "tagline": {
            "id": "Belajar langsung bagaimana operasional perusahaan berjalan di lapangan.",
            "en": "Learning first-hand how company operations run on site.",
        },
        "points": {
            "id": [
                "Magang di bidang **manajemen dan operasional** secara **langsung di lokasi** perusahaan di Jakarta Barat.",
                "Mendukung **kegiatan operasional harian** dan belajar **alur kerja serta koordinasi antartim**.",
            ],
            "en": [
                "Interned in **management and operations**, working **on site** at the company's office in West Jakarta.",
                "Supported **day-to-day operations** and learned **workflows and cross-team coordination**.",
            ],
        },
        "tags": ["Onsite Management", "Operations Management"],
    },
]

ORGANIZATIONS = [
    {
        "title": "Himpunan Teknik Informatika (HMTI)",
        "role": "Public Relations",
        "period": {"id": "Okt 2024 — Apr 2026", "en": "Oct 2024 — Apr 2026"},
        "tagline": {
            "id": "Jembatan antara acara, sponsor, dan sorotan media.",
            "en": "The bridge between events, sponsors, and the media spotlight.",
        },
        "points": {
            "id": [
                "Bergabung sebagai **Public Relations** di Himpunan Teknik Informatika selama **1,5 tahun**, bertanggung jawab atas komunikasi eksternal organisasi.",
                "Membangun dan menjaga relasi dengan **sponsor** serta **media partner** untuk mendukung kesuksesan setiap acara himpunan.",
                "Menyusun **pesan komunikasi yang menarik** dan mengoordinasikan kolaborasi untuk meningkatkan **visibilitas acara**.",
            ],
            "en": [
                "Served as **Public Relations** at the Informatics Engineering Student Association for **1.5 years**, handling the organization's external communication.",
                "Built and maintained relationships with **sponsors** and **media partners** to support the success of every association event.",
                "Crafted **compelling messaging** and coordinated collaborations to boost **event visibility**.",
            ],
        },
        "tags": ["Public Relations", "Partnership", "Communication"],
        "photos": [
            {"src": "lanyard.png", "caption": {"id": "Himpunan Mahasiswa Teknik Informatika", "en": "Himpunan Mahasiswa Teknik Informatika"}},
            {"src": "org-2.png", "caption": {"id": "Dokumentasi Kepengurusan HIMTI", "en": "HIMTI Team Documentation"}},
        ],
        # sertifikat tampil melebar di bawah foto, dengan label "Lihat Sertifikat"
        "certificate": {
            "src": "org-cert.jpg",
            "caption": {"id": "Sertifikat Kepengurusan HIMTI", "en": "HIMTI certificate"},
        },
    },
    {
        "title": "Seminar SYNC 2025 — HIMTI",
        "role": {"id": "Tim Registrasi & Operasional", "en": "Registration & Operations Team"},
        "period": {"id": "24 Agustus 2025", "en": "24 August 2025"},
        "tagline": {
            "id": "Dari meja registrasi sampai acara berjalan mulus.",
            "en": "From the registration desk to a seamless event.",
        },
        "points": {
            "id": [
                "Menjadi bagian dari **tim registrasi & operasional** Seminar SYNC 2025 yang diselenggarakan HIMTI pada **24 Agustus 2025**.",
                "Bertanggung jawab atas **registrasi peserta** secara langsung di lokasi dan mendukung **kelancaran operasional** dari awal hingga akhir, berkoordinasi dengan tim lain.",
                "Mendokumentasikan jalannya kegiatan dan mengunggah **live report** di Instagram **@kariralumni.umb**.",
            ],
            "en": [
                "Part of the **registration & operations team** for Seminar SYNC 2025, organized by HIMTI on **24 August 2025**.",
                "Handled on-site **participant registration** and supported **smooth operations** from start to finish, coordinating with other teams.",
            ],
        },
        "tags": ["Event", "Registration", "Operations"],
        "photos": [
            {"src": "event-sync-1.jpg", "caption": {"id": "Suasana registrasi peserta Seminar SYNC 2025", "en": "Participant registration at Seminar SYNC 2025"}},
            {"src": "event-sync-2.jpg", "caption": {"id": "Tim operasional Seminar SYNC 2025", "en": "Seminar SYNC 2025 operations team"}},
            {"src": "event-sync-3.jpg", "caption": {"id": "Dokumentasi jalannya seminar", "en": "Seminar proceedings documentation"}},
            {"src": "sync.himti.jpg", "caption": {"id": "Foto Bersama Peserta dan Panitia", "en": "Group Photo of Participants and Organizers"}},
        ],
    },
    {
        "title": "Mercu Buana Career Expo 2025",
        "role": {"id": "Tim Dokumentasi", "en": "Documentation Team"},
        "period": {"id": "26–27 September 2025", "en": "26–27 September 2025"},
        "tagline": {
            "id": "Mengabadikan dua hari penuh energi karier.",
            "en": "Capturing two days full of career energy.",
        },
        "points": {
            "id": [
                "Bertugas di **tim dokumentasi** Mercu Buana Career Expo 2025 selama **dua hari penyelenggaraan** (26–27 September 2025).",
                "Mendokumentasikan seluruh rangkaian acara dan mengunggah **live report real-time** ke Instagram **@kariralumni.umb**.",
                "Berkoordinasi dengan tim penyelenggara agar **momen-momen penting** acara terekam dengan baik.",
            ],
            "en": [
                "Served on the **documentation team** of Mercu Buana Career Expo 2025 across **two full event days** (26–27 September 2025).",
                "Documented the entire program and posted **real-time live reports** on Instagram **@kariralumni.umb**.",
                "Coordinated with the organizing team to make sure **key moments** were captured.",
            ],
        },
        "tags": ["Event", "Documentation", "Live Report"],
        "photos": [
            {"src": "event-expo-1.jpg", "caption": {"id": "Suasana Mercu Buana Career Expo 2025", "en": "Mercu Buana Career Expo 2025 atmosphere"}},
            {"src": "event-expo-2.jpg", "caption": {"id": "Booth peserta career expo", "en": "Career expo participant booths"}},
            {"src": "event-expo-3.jpg", "caption": {"id": "Team of Event", "en": "Panitia Acara"}},
            {"src": "event-expo-4.jpg", "caption": {"id": "Live report di Instagram @kariralumni.umb", "en": "Live report on @kariralumni.umb Instagram"}},
        ],
    },
    {
        "title": "Career Readiness & Future Skill 2025 — Kemnaker",
        "role": {"id": "Operator Presentasi (Tampilan Materi)", "en": "Presentation / Screen Operator"},
        "period": {"id": "29 Oktober 2025", "en": "29 October 2025"},
        "tagline": {
            "id": "Memastikan setiap slide tampil tepat pada waktunya.",
            "en": "Making sure every slide lands at exactly the right moment.",
        },
        "points": {
            "id": [
                "Berperan sebagai **operator presentasi** pada seminar **Career Readiness & Future Skill 2025** bersama **Kemnaker** (29 Oktober 2025).",
                "Mengoperasikan **tampilan materi** narasumber di layar selama acara berlangsung.",
                "Memastikan **slide tersinkronisasi** dengan alur pemaparan setiap pembicara.",
            ],
            "en": [
                "Acted as **presentation operator** at the **Career Readiness & Future Skill 2025** seminar with **Kemnaker** (29 October 2025).",
                "Operated the on-screen **display of speakers' materials** throughout the session.",
                "Kept **slides in sync** with each speaker's flow of discussion.",
            ],
        },
        "tags": ["Event", "Operator", "Technical Support"],
        "photos": [
            {"src": "event-kemnaker-1.jpg", "caption": {"id": "Sesi Konseling Karir", "en": "Career counseling session"}},
            {"src": "event-kemnaker-2.jpg", "caption": {"id": "Foto bersama Tim Mercu Buana bersama Kemnaker", "en": "Group photo of the Mercu Buana team with the Ministry of Manpower."}},
        ],
    },
    {
        "title": "Seminar Softskill: “Public Speaking” — Biro Karir UMB",
        "role": {"id": "Dokumentasi", "en": "Documentation"},
        "period": {"id": "23 Oktober 2025", "en": "23 October 2025"},
        "tagline": {
            "id": "Mengabadikan momen belajar berbicara di depan publik.",
            "en": "Capturing the moments of learning to speak in public.",
        },
        "points": {
            "id": [
                "Bertugas sebagai **dokumentasi** pada Seminar Softskill **“Public Speaking”** yang diselenggarakan Biro Karir, Hubungan dan Penelusuran Alumni UMB (23 Oktober 2025).",
                "Mengabadikan **interaksi peserta dan pembicara** dari awal hingga akhir untuk kebutuhan **publikasi Biro Karir**.",
            ],
            "en": [
                "Served as **documentation** for the **“Public Speaking”** softskill seminar by the UMB Career, Alumni Relations & Tracing Bureau (23 October 2025).",
                "Captured **participant–speaker interactions** from start to finish for the **career bureau's publications**.",
            ],
        },
        "tags": ["Event", "Documentation", "Softskill"],
        "photos": [
            {"src": "event-publicspeaking-1.jpg", "caption": {"id": "Suasana seminar Public Speaking", "en": "Public Speaking seminar atmosphere"}},
            {"src": "event-publicspeaking-2.jpg", "caption": {"id": "Team of Event", "en": "Panitia Acara"}},
        ],
    },
    {
        "title": "Industrial Talk — Biro Karir UMB x Gojek & Tokopedia",
        "role": {"id": "MC", "en": "Master of Ceremony"},
        "period": {"id": "30 April 2026", "en": "30 April 2026"},
        "tagline": {
            "id": "Memandu percakapan antara kampus dan industri.",
            "en": "Hosting the conversation between campus and industry.",
        },
        "points": {
            "id": [
                "Bertugas sebagai **MC** pada **Industrial Talk** Biro Karir UMB bersama **Gojek & Tokopedia** (30 April 2026).",
                "Memandu jalannya acara di hadapan peserta dan **narasumber dari Gojek dan Tokopedia**, menjaga suasana tetap **interaktif**.",
                "Memastikan seluruh sesi berjalan **tepat waktu** sesuai rundown.",
            ],
            "en": [
                "Served as **MC** of the **Industrial Talk** by the UMB Career Bureau with **Gojek & Tokopedia** (30 April 2026).",
                "Hosted the program in front of participants and **speakers from Gojek and Tokopedia**, keeping the atmosphere **interactive**.",
                "Kept every session **on schedule** according to the rundown.",
            ],
        },
        "tags": ["Event", "MC", "Public Speaking"],
        "photos": [
            {"src": "event-industrialtalk1-1.jpg", "caption": {"id": "MC Industrial Talk bersama Gojek & Tokopedia", "en": "MC at Industrial Talk with Gojek & Tokopedia"}},
            {"src": "event-industrialtalk1-3.jpg", "caption": {"id": "Sertifikat", "en": "Certificate"}},
            {"src": "event-industrialtalk1-2.jpg", "caption": {"id": "Dokumentasi bersama narasumber", "en": "Documentation with the speakers"}},
        ],
    },
    {
        "title": "Seminar Softskill Karir & Networking — Biro Karir UMB",
        "role": {"id": "MC", "en": "Master of Ceremony"},
        "period": {"id": "7 Mei 2026", "en": "7 May 2026"},
        "tagline": {
            "id": "Membuka ruang obrolan karier yang hangat.",
            "en": "Opening a warm space for career conversations.",
        },
        "points": {
            "id": [
                "Bertugas sebagai **MC** pada **Seminar Softskill Karir & Networking** Biro Karir UMB (7 Mei 2026).",
                "Memandu jalannya seminar dan membantu menciptakan suasana **interaktif** antara peserta dan pembicara.",
            ],
            "en": [
                "Served as **MC** of the **Career & Networking Softskill Seminar** by the UMB Career Bureau (7 May 2026).",
                "Guided the seminar and helped create an **interactive atmosphere** between participants and speakers.",
            ],
        },
        "tags": ["Event", "MC", "Networking"],
        "photos": [
            {"src": "event-networking-1.jpg", "caption": {"id": "MC Seminar Karir & Networking", "en": "MC at Career & Networking Seminar"}},
            {"src": "event-networking-2.jpg", "caption": {"id": "Suasana seminar", "en": "Seminar atmosphere"}},
            {"src": "event-networking-3.jpg", "caption": {"id": "Dokumentasi bersama narasumber", "en": "Documentation with the speakers"}},
        ],
    },
    {
        "title": "Industrial Talk — Biro Karir UMB x PT Digdeep",
        "role": {"id": "MC", "en": "Master of Ceremony"},
        "period": {"id": "20 Mei 2026", "en": "20 May 2026"},
        "tagline": {
            "id": "Menjaga percakapan industri tetap hidup dan tepat waktu.",
            "en": "Keeping the industry conversation lively and on time.",
        },
        "points": {
            "id": [
                "Bertugas sebagai **MC** pada **Industrial Talk** Biro Karir UMB bersama **PT Digdeep** (20 Mei 2026).",
                "Memandu jalannya acara dan menjaga alur tetap **interaktif** serta sesuai **rundown** dari awal hingga akhir.",
            ],
            "en": [
                "Served as **MC** of the **Industrial Talk** by the UMB Career Bureau with **PT Digdeep** (20 May 2026).",
                "Hosted the program and kept the flow **interactive** and on track with the **rundown** from start to finish.",
            ],
        },
        "tags": ["Event", "MC", "Public Speaking"],
        "photos": [
            {"src": "event-industrialtalk2-1.jpg", "caption": {"id": "Dokumentasi bersama narasumber", "en": "Documentation with the speakers"}},
            {"src": "event-industrialtalk2-2.jpg", "caption": {"id": "Suasana sesi Industrial Talk", "en": "Industrial Talk session atmosphere"}},
            {"src": "event-industrialtalk2-3.jpg", "caption": {"id": "Sertifikat", "en": "Certificate"}},
        ],
    },
    {
        "title": "Kuliah Umum — PT. Rindang Kurnia Motor & ALVA",
        "role": {"id": "Dokumentasi", "en": "Documentation"},
        "period": {"id": "25 Juni 2026", "en": "25 June 2026"},
        "tagline": {
            "id": "Merekam ilmu dari praktisi industri untuk kampus.",
            "en": "Capturing industry practitioners' insights for campus.",
        },
        "points": {
            "id": [
                "Bertugas sebagai **dokumentasi** pada **Kuliah Umum** bersama **PT. Rindang Kurnia Motor & ALVA** (25 Juni 2026).",
                "Mengabadikan **momen-momen penting** acara untuk kebutuhan **publikasi dan arsip** Biro Karir.",
            ],
            "en": [
                "Served as **documentation** for the **General Lecture** with **PT. Rindang Kurnia Motor & ALVA** (25 June 2026).",
                "Captured **key moments** of the event for the career bureau's **publication and archive** needs.",
            ],
        },
        "tags": ["Event", "Documentation", "Guest Lecture"],
        "photos": [
            {"src": "event-kuliahumum-1.jpg", "caption": {"id": "Dokumentasi bersama narasumber", "en": "Documentation with the speakers"}},
            {"src": "event-kuliahumum-2.jpg", "caption": {"id": "Dokumentasi kegiatan", "en": "Event documentation"}},
        ],
    },
]

PROJECTS = [
    {
        "title": "Dormi — Dormitory Management System",
        "description": {
            "id": "Sistem manajemen asrama berbasis web dengan klasifikasi laporan darurat otomatis dan chatbot NLP dwibahasa.",
            "en": "Web-based dormitory management system with automatic emergency-report classification and a bilingual NLP chatbot.",
        },
        "purpose": {
            "id": "Dibangun sebagai **tugas akhir (skripsi)** untuk membantu pengelola asrama menangani **laporan darurat penghuni** secara lebih cepat dan terstruktur, lewat klasifikasi otomatis dan chatbot yang membantu penghuni berinteraksi dengan sistem.",
            "en": "Built as my **undergraduate thesis** to help dormitory managers handle **residents' emergency reports** faster and in a more structured way, through automatic classification and a chatbot that helps residents interact with the system.",
        },
        # "partner" opsional — hapus saja kalau proyeknya tanpa mitra
        "features": {
            "id": [
                "**Klasifikasi otomatis laporan darurat** ke dalam **5 kategori** memakai Multinomial Naive Bayes + TF-IDF.",
                "Akurasi model **93.65%** dengan macro avg F1-score **0.93** dari **1.259 data latih**.",
                "**Chatbot NLP dwibahasa** untuk membantu interaksi penghuni dengan sistem.",
                "Lolos **black box testing 17/17 skenario** (100%).",
            ],
            "en": [
                "**Automatic emergency-report classification** into **5 categories** using Multinomial Naive Bayes + TF-IDF.",
                "Model accuracy of **93.65%** with a macro avg F1-score of **0.93** from **1,259 training data points**.",
                "**Bilingual NLP chatbot** that helps residents interact with the system.",
                "Passed **black box testing on 17/17 scenarios** (100%).",
            ],
        },
        "tech": ["Python", "Machine Learning", "NLP", "Multinomial Naive Bayes", "TF-IDF"],
        "images": [
            {"src": "dormi-1.jpg", "caption": {"id": "Tampilan sistem Dormi", "en": "Dormi system overview"}},
            {"src": "dormi-2.jpg", "caption": {"id": "Hasil klasifikasi laporan darurat", "en": "Emergency report classification result"}},
            {"src": "dormi-3.jpg", "caption": {"id": "Chatbot", "en": "Bilingual chatbot"}},
            {"src": "dormi-4.jpg", "caption": {"id": "Admin panel", "en": "Admin panel"}},
        ],
        "github": "https://github.com/username-kamu/dormi",  # ganti link repo asli
        "demo": "",  # isi link demo kalau ada, kosongkan kalau tidak ada
    },
    {
        "title": "Digital Attendance System",
        "description": {
            "id": "Sistem absensi digital berbasis web untuk perusahaan dengan skema kerja hybrid/remote.",
            "en": "Web-based digital attendance system for companies with hybrid/remote work arrangements.",
        },
        "purpose": {
            "id": "Dibangun untuk membantu perusahaan dengan skema kerja **hybrid/remote** mencatat kehadiran karyawan secara **digital dan real-time**, sekaligus memudahkan tim HR memantau dan menganalisis kehadiran.",
            "en": "Built to help companies with **hybrid/remote** work arrangements record employee attendance **digitally and in real time**, while making it easier for the HR team to monitor and analyze attendance.",
        },
        "partner": {
            "name": "PT. Winnicode Garuda Teknologi",
            "about": {
                "id": "Perusahaan berbasis di **Yogyakarta** tempat aku mengerjakan proyek ini sebagai **Fullstack Developer** (WFH, Feb–Mei 2025). Sistemnya dirancang untuk perusahaan di **industri media digital**.",
                "en": "A **Yogyakarta**-based company where I worked on this project as a **Fullstack Developer** (WFH, Feb–May 2025). The system is designed for companies in the **digital media industry**.",
            },
        },
        "features": {
            "id": [
                "**Pencatatan absensi digital** untuk karyawan hybrid/remote.",
                "**Pengajuan izin/cuti online**.",
                "**Dashboard monitoring HR real-time**.",
                "**Laporan analitik kehadiran**.",
                "Menyusun **proposal proyek**: kebutuhan sistem, scope, tech stack, dan timeline pengembangan.",
            ],
            "en": [
                "**Digital attendance recording** for hybrid/remote employees.",
                "**Online leave/permission requests**.",
                "**Real-time HR monitoring dashboard**.",
                "**Attendance analytics reporting**.",
                "Authored the **project proposal**: system requirements, scope, tech stack, and development timeline.",
            ],
        },
        "tech": ["React.js", "Next.js", "Laravel", "MySQL"],
        "images": [
            {"src": "attendance-1.jpg", "caption": {"id": "Tampilan awal", "en": "Preview Screens"}},
            {"src": "attendance-2.jpg", "caption": {"id": "Laporan Absensi Harian", "en": "Daily Attendance Report"}},
            {"src": "attendance-3.jpg", "caption": {"id": "Manajemen Data Pegawai", "en": "Employee Data Management"}},
        ],
        "github": "https://github.com/nisaica1910/Absensi-Magang-WinniCode.git",  # proyek perusahaan biasanya private; isi kalau repo-nya boleh dibuka
        "demo": "",
    },
    {
        "title": "MEMORA — AWS Chatbot",
        "description": {
            "id": "Chatbot berbasis AWS yang memberikan respons efisien dan cerdas.",
            "en": "AWS-based chatbot delivering efficient and intelligent responses.",
        },
        "purpose": {
            "id": "Dibangun sebagai **proyek capstone** program RevoU Cloud and Gen AI Machine Learning: chatbot yang memberikan **respons efisien dan cerdas** dan berjalan di infrastruktur **AWS**.",
            "en": "Built as the **capstone project** of the RevoU Cloud and Gen AI Machine Learning program: a chatbot that delivers **efficient and intelligent responses**, running on **AWS** infrastructure.",
        },
        "partner": {
            "name": "RevoU",
            "about": {
                "id": "Penyelenggara program **Studi Independen Kampus Merdeka** (Kemendikbud) **Cloud and Gen AI Machine Learning**, Sep–Des 2024, tempat proyek ini dikerjakan.",
                "en": "Provider of the **Kampus Merdeka Independent Study** program (Ministry of Education) **Cloud and Gen AI Machine Learning**, Sep–Dec 2024, where this project was built.",
            },
        },
                "features": {
            "id": [
                "**Chatbot RAG berbasis AWS (EC2)** yang menjawab pertanyaan secara efisien dan kontekstual.",
                "**Upload dokumen (TXT, PDF, DOCX)** hingga 200MB per file, lalu chatbot menjawab berdasarkan isi dokumen tersebut.",
                "**Manajemen riwayat chat**: buat chat baru, pilih chat sebelumnya, dan hapus chat yang tidak diperlukan.",
                "**Pengaturan respons fleksibel**: batas jumlah kata output (10–500) dan *temperature* (0.00–1.00).",
                "**Pilihan behavior** (misalnya Professional dan Humorous) serta fitur **Vibe Up!** untuk menyesuaikan gaya jawaban lewat instruksi sendiri.",
                "Dikerjakan tim dengan **perencanaan proyek, pembagian tugas, dan milestone** yang saya koordinasikan sebagai Project Leader.",
                "Diakui sebagai salah satu **Top 2 Best Teams**.",
            ],
            "en": [
                "**AWS-based (EC2) RAG chatbot** that answers questions efficiently and contextually.",
                "**Document upload (TXT, PDF, DOCX)** up to 200MB per file, with answers grounded in the document's content.",
                "**Chat history management**: start a new chat, switch between past chats, and delete the ones you no longer need.",
                "**Flexible response controls**: output word limit (10–500) and *temperature* (0.00–1.00).",
                "**Selectable behavior** (e.g., Professional and Humorous) plus a **Vibe Up!** feature to customize the answer style with your own instructions.",
                "Built by a team with **project planning, task distribution, and milestones** that I coordinated as Project Leader.",
                "Recognized as one of the **Top 2 Best Teams**.",
            ],
        },
        "tech": ["AWS", "Machine Learning", "Chatbot"],
        "images": [
            {"src": "memora-1.jpg", "caption": {"id": "Tampilan chatbot MEMORA", "en": "MEMORA chatbot interface"}},
            {"src": "memora-2.jpg", "caption": {"id": "Manajemen Riwayat Obrolan", "en": "Chat History Management"}},
            {"src": "memora-3.jpg", "caption": {"id": "Custom sifat chatbot", "en": "Custom Behaviors"}},
        ],
        "github": "https://github.com/nisaica1910/Memora-Chatbot.git",  # ganti link repo asli
        "demo": "",
    },
        {
        "title": "MamiNa — Website Bimbel Mewarnai & Menggambar",
        "description": {
            "id": "Website bimbel mewarnai dan menggambar anak dengan pendaftaran online, dashboard admin, dan galeri karya anak.",
            "en": "Website for a children's coloring and drawing class, with online registration, an admin dashboard, and a gallery of kids' artwork.",
        },
        "purpose": {
            "id": "Dibangun sebagai **website bisnis** untuk bimbel mewarnai dan menggambar anak: calon murid bisa **melihat kelas dan mendaftar online**, sementara pemilik mengelola **pendaftar, murid, absensi, dan pembayaran** lewat **dashboard admin**.",
            "en": "Built as a **business website** for a children's coloring and drawing class: prospective students can **browse classes and register online**, while the owner manages **registrations, students, attendance, and payments** through an **admin dashboard**.",
        },
        "features": {
            "id": [
                "**Landing page ramah anak** dengan desain pastel yang ceria dan navigasi sederhana (Kelas, Karya anak, Lokasi, Daftar, Admin).",
                "**Katalog 3 kelas** (Mewarnai Basic, Mewarnai Lanjutan, Menggambar) lengkap dengan harga per jam, durasi, jadwal, dan **sisa kursi yang diperbarui otomatis**.",
                "**Formulir pendaftaran online** berisi data anak dan kontak orang tua, dengan alur bergabung 3 langkah: isi formulir, dikonfirmasi via WhatsApp, lalu mulai mewarnai.",
                "**Integrasi WhatsApp**: tombol *Tanya lewat WhatsApp* yang selalu tampil dan tombol *Chat WhatsApp* untuk konfirmasi jadwal.",
                "**Dashboard admin** dengan ringkasan bulanan (pendaftar baru, murid aktif, tunggakan, pembayaran masuk) dan **kuota tiap kelas**.",
                "**Manajemen operasional** lewat menu Pendaftar, Murid, Kelas, Absensi, Pembayaran, dan Karya, serta login admin.",
                "**Galeri karya anak** untuk memajang hasil karya murid.",
                "**Peta lokasi** studio yang terhubung dengan Google Maps.",
                "Dirancang dan dibangun sendiri, dari **desain UI, frontend, backend, hingga database**.",
            ],
            "en": [
                "**Kid-friendly landing page** with a cheerful pastel design and simple navigation (Classes, Kids' Work, Location, Register, Admin).",
                "**Catalog of 3 classes** (Basic Coloring, Advanced Coloring, Drawing) with hourly price, duration, schedule, and **automatically updated seat availability**.",
                "**Online registration form** for the child's details and parent contact, with a 3-step joining flow: fill in the form, get confirmed via WhatsApp, then start coloring.",
                "**WhatsApp integration**: an always-visible *Ask via WhatsApp* button and a *Chat WhatsApp* button for schedule confirmation.",
                "**Admin dashboard** with a monthly summary (new registrations, active students, unpaid this month, payments received) and **per-class quota**.",
                "**Operational management** through Registrants, Students, Classes, Attendance, Payments, and Artwork menus, plus admin login.",
                "**Kids' artwork gallery** to proudly showcase student work.",
                "**Location map** of the studio embedded with Google Maps.",
                "Designed and built end to end, from **UI design and frontend to backend and database**.",
            ],
        },
        "tech": ["Python", "Flask", "HTML/CSS", "JavaScript", "Google Maps"],
        "images": [
            {"src": "mamina-1.jpg", "caption": {"id": "Halaman utama MamiNa", "en": "MamiNa landing page"}},
            {"src": "mamina-2.jpg", "caption": {"id": "Pilihan kelas dan cara bergabung", "en": "Class options and how to join"}},
            {"src": "mamina-3.jpg", "caption": {"id": "Lokasi studio dan kontak WhatsApp", "en": "Studio location and WhatsApp contact"}},
            {"src": "mamina-4.jpg", "caption": {"id": "Dashboard admin", "en": "Admin dashboard"}},
        ],
        "github": "https://github.com/nisaica1910/MamiNa-Bimbel-Website.git",
        "demo": "",
    },
        {
        "title": "A STUDIO — Website Company Profile",
        "description": {
            "id": "Website company profile untuk studio desain dan kontraktor interior, lengkap dengan portofolio proyek dan dashboard admin untuk mengelola konten.",
            "en": "A company profile website for an interior design and contractor studio, with a project portfolio and an admin dashboard for managing content.",
        },
        "purpose": {
            "id": "Dibangun sebagai **website company profile** untuk studio desain dan kontraktor interior: calon klien bisa **melihat layanan dan proyek pilihan** lalu **menghubungi lewat konsultasi gratis atau WhatsApp**, sementara admin mengelola **proyek, kategori, dan pesan masuk** lewat **dashboard admin** tanpa mengubah kode.",
            "en": "Built as a **company profile website** for an interior design and contractor studio: prospective clients can **browse services and featured projects** and **get in touch through a free consultation or WhatsApp**, while the admin manages **projects, categories, and incoming messages** through an **admin dashboard** without touching the code.",
        },
        "features": {
            "id": [
                "**Landing page profesional** dengan hero, bagian Tentang Kami, Layanan, Proyek pilihan, dan Proses Kerja dari konsultasi hingga serah terima.",
                "**Etalase portofolio proyek** yang dikelompokkan per kategori (Interior Rumah dan Interior Kantor), dengan halaman daftar semua proyek.",
                "**Tombol WhatsApp** yang selalu tampil dan tombol *Konsultasi Gratis* di setiap halaman untuk memudahkan calon klien menghubungi.",
                "**Dashboard admin** dengan ringkasan total proyek, proyek tayang dan draft, jumlah per kategori, serta pesan masuk.",
                "**Manajemen konten** lewat menu Proyek, Pesan, dan Pengaturan, dilengkapi login admin.",
                "**Pengelolaan proyek dan kategori**, termasuk status tayang atau draft untuk setiap proyek.",
                "**Unggah gambar dengan pengubahan ukuran otomatis** agar tampilan portofolio tetap rapi dan ringan.",
                "**Formulir kontak** yang pesannya langsung tersimpan dan tampil di dashboard admin.",
                "Menggunakan **database SQLite** dan sudah **dipublikasikan secara online**.",
            ],
            "en": [
                "**Professional landing page** with a hero, About Us, Services, Featured Projects, and a Work Process section from consultation to handover.",
                "**Project portfolio showcase** grouped by category (Home Interior and Office Interior), with a page listing all projects.",
                "**Always-visible WhatsApp button** and a *Free Consultation* button on every page to make it easy for prospects to reach out.",
                "**Admin dashboard** with a summary of total projects, published and draft projects, per-category counts, and incoming messages.",
                "**Content management** through Projects, Messages, and Settings menus, with admin login.",
                "**Project and category management**, including a published or draft status for each project.",
                "**Image upload with automatic resizing** to keep the portfolio looking neat and loading fast.",
                "**Contact form** whose messages are saved and shown in the admin dashboard.",
                "Uses an **SQLite database** and is **deployed online**.",
            ],
        },
        "tech": ["Python", "Flask", "PostgreSQL", "HTML/CSS", "JavaScript"],
        "images": [
            {"src": "astudio-0.jpg", "caption": {"id": "Preview Website", "en": "Mockup of A STUDIO landing page"}},
            {"src": "astudio-1.jpg", "caption": {"id": "Halaman utama A STUDIO", "en": "A STUDIO landing page"}},
            {"src": "astudio-3.jpg", "caption": {"id": "Layanan yang ditawarkan", "en": "Services offered"}},
            {"src": "astudio-4.jpg", "caption": {"id": "Proyek pilihan", "en": "Featured projects"}},
            {"src": "astudio-5.jpg", "caption": {"id": "Proses kerja", "en": "Work process"}},
            {"src": "astudio-6.jpg", "caption": {"id": "Dashboard admin", "en": "Admin dashboard"}},
        ],
        "github": "",
        "demo": "https://website-a-studio.onrender.com",
    },
]

CERTIFICATES = [
    {"title": "Sertifikat Kompetensi Software Engineer — BNSP (2026)", "image": "cert-0.jpg", "link": "#"},
    {"title": "Machine Learning with Python — IBM (Coursera, 2026)", "image": "cert-1.jpg", "link": "#"},
    {"title": "MSIB Studi Independen Bersertifikat  — MBKM (2024)", "image": "cert-2.jpg", "link": "#"},
    {"title": "AWS Cloud Practitioner Essentials — AWS (2024)", "image": "cert-3.jpg", "link": "#"},
    {"title": "Machine Learning Essentials for Business and Technical Decision Makers (2024)", "image": "cert-4.jpg", "link": "#"},
    {"title": "Best Capstone Project Team — RevoU (2024)", "image": "cert-5.jpg", "link": "#"},
    {"title": "CERTIFICATE OF COMPLETION Cloud And Gen AI Machine Learning By RevoU— RevoU (2024)", "image": "cert-6.jpg", "link": "#"},
    {"title": "Planning a Machine Learning Project — AWS (2024)", "image": "cert-7.jpg", "link": "#"},
]

@app.template_filter("bold")
def bold_filter(text):
    """Ubah **teks** jadi <strong>teks</strong> (aman dari HTML injection)."""
    safe = str(escape(text))
    return Markup(re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", safe))

def _resolve(node, lang):
    """Walk the data structures above and turn every {'id': .., 'en': ..}
    leaf into the plain string/list for the requested language."""
    if isinstance(node, dict):
        if set(node.keys()) == {"id", "en"}:
            return node.get(lang, node["id"])
        return {k: _resolve(v, lang) for k, v in node.items()}
    if isinstance(node, list):
        return [_resolve(v, lang) for v in node]
    return node


@app.route("/")
def home():
    lang = request.args.get("lang", "id")
    if lang not in ("id", "en"):
        lang = "id"

    all_items = _resolve(ORGANIZATIONS, lang)

    return render_template(
        "index.html",
        lang=lang,
        ui=_resolve(UI_STRINGS, lang),
        profile=_resolve(PROFILE, lang),
        pillars=_resolve(PILLARS, lang),
        skills=_resolve(SKILLS, lang),
        experiences=_resolve(EXPERIENCES, lang),
        # item yang punya tag "Event" masuk ke bagian Event, sisanya ke bagian Organisasi
        organizations=[o for o in all_items if "Event" not in o["tags"]],
        events=[o for o in all_items if "Event" in o["tags"]],
        projects=_resolve(PROJECTS, lang),
        certificates=_resolve(CERTIFICATES, lang),
        roles=_resolve(ROLE_LABELS, lang),
    )

if __name__ == "__main__":
    app.run(debug=True)
