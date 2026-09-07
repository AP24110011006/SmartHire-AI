/*==========================================================
    SmartHire AI v2.0
    script.js
==========================================================*/

"use strict";

/*==========================================================
    DOM ELEMENTS
==========================================================*/

const resumeInput = document.getElementById("resumeInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const uploadArea = document.getElementById("uploadArea");

const loading = document.getElementById("loading");
const dashboard = document.getElementById("dashboard");

const resumePreview = document.getElementById("resumePreview");

/* Candidate */

const candidateName = document.getElementById("candidateName");
const candidateEmail = document.getElementById("candidateEmail");
const candidatePhone = document.getElementById("candidatePhone");
const prediction = document.getElementById("prediction");

/* Scores */

const resumeScoreCircle = document.getElementById("resumeScoreCircle");
const atsScoreCircle = document.getElementById("atsScoreCircle");
const confidenceCircle = document.getElementById("confidenceCircle");

/* Career */

const salaryBand = document.getElementById("salaryBand");
const careerLevel = document.getElementById("careerLevel");
const interviewReadiness = document.getElementById("interviewReadiness");
const skillsToLearn = document.getElementById("skillsToLearn");

/* Jobs */

const recommendedJobs = document.getElementById("recommendedJobs");

/* Suggestions */

const suggestions = document.getElementById("suggestions");

/* Statistics */

const skillCount = document.getElementById("skillCount");
const educationCount = document.getElementById("educationCount");
const experienceCount = document.getElementById("experienceCount");

/* Report */

const downloadReport = document.getElementById("downloadReport");

const selectedFile = document.getElementById("selectedFile");

const toast = document.getElementById("toast");

const toastMessage = document.getElementById("toastMessage");

/*==========================================================
    GLOBAL VARIABLES
==========================================================*/

let uploadedFile = null;

let responseData = null;

/*==========================================================
    FILE UPLOAD
==========================================================*/

resumeInput.addEventListener("change", function () {

    if (this.files.length === 0) return;

    handleFile(this.files[0]);

});


uploadArea.addEventListener("dragover", function (e) {

    e.preventDefault();

    uploadArea.style.borderColor = "#10B981";

});


uploadArea.addEventListener("dragleave", function () {

    uploadArea.style.borderColor = "rgba(16,185,129,.35)";

});


uploadArea.addEventListener("drop", function (e) {

    e.preventDefault();

    uploadArea.style.borderColor = "rgba(16,185,129,.35)";

    const file = e.dataTransfer.files[0];

    if (file) {

        resumeInput.files = e.dataTransfer.files;

        handleFile(file);

    }

});


/*==========================================================
    HANDLE FILE
==========================================================*/

function handleFile(file) {

    if (!file) {

        showToast("Please select a resume.");

        return;

    }

    const allowed = [

        "application/pdf",

        "application/msword",

        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    ];

    if (!allowed.includes(file.type)) {

        showToast("Please upload PDF, DOC or DOCX.");

        return;

    }

    uploadedFile = file;

    resetDashboard();

    // Save filename for current browser session
    sessionStorage.setItem("resumeName", file.name);

    // Display selected filename
    selectedFile.textContent = "📄 " + file.name;

    // Preview the uploaded resume
    previewResume(file);

    // Success notification
    showToast("Resume uploaded successfully!");

}


/*==========================================================
    PREVIEW
==========================================================*/

function previewResume(file) {

    if (file.type === "application/pdf") {

        const url = URL.createObjectURL(file);

        resumePreview.src = url;

    }

    else {

        resumePreview.src = "";

    }

}

/*==========================================================
    ANALYZE BUTTON
==========================================================*/

analyzeBtn.addEventListener("click", function () {

    console.log("Analyze button clicked");

    console.log(uploadedFile);

    if (!uploadedFile) {

        showToast("Please upload a resume first.");

        return;

    }

    analyzeResume();

});

/*==========================================================
    API CALL
==========================================================*/

/*==========================================================
    ANALYZE RESUME
==========================================================*/

async function analyzeResume() {

    try {

        loading.classList.remove("hidden");

        dashboard.classList.add("hidden");

        analyzeBtn.disabled = true;

        const formData = new FormData();

        formData.append("resume", uploadedFile);

        const response = await fetch("/predict", {

            method: "POST",

            body: formData

        });

        if (!response.ok) {

            throw new Error("Prediction failed");

        }

        responseData = await response.json();

        if (responseData.status !== "success") {

            throw new Error("Backend returned an error.");

        }

        loading.classList.add("hidden");

        dashboard.classList.remove("hidden");

        analyzeBtn.disabled = false;

        updateDashboard(responseData);

        dashboard.scrollIntoView({

            behavior: "smooth",

            block: "start"

        });

        showToast("Resume analyzed successfully!");

    }

    catch (err) {

        console.error(err);

        loading.classList.add("hidden");

        dashboard.classList.add("hidden");

        analyzeBtn.disabled = false;

        showToast("Analysis failed. Please try again.");

    }

}

/*==========================================================
    UPDATE DASHBOARD
==========================================================*/

function updateDashboard(data){

    console.log("Dashboard Data:", data);

    updateCandidate(data);

    updateScores(data);

    updateCareerInsights(data);

    updateSuggestions(data);

    updateStatistics(data);

    updateJobs(data);

    animateCards();

    //celebrate(data.resume_score.score);

}
/*==========================================================
    CANDIDATE INFORMATION
==========================================================*/

function updateCandidate(data){

    const info = data.analysis || {};

    candidateName.textContent =
        info.name || "Not Available";

    candidateEmail.textContent =
        info.email || "Not Available";

    candidatePhone.textContent =
        info.phone || "Not Available";

    prediction.textContent =
        data.category || "Unknown";

}

/*==========================================================
    SCORES
==========================================================*/

function updateScores(data){

    animateScore(
        resumeScoreCircle,
        data.resume_score.score
    );

    animateScore(
        atsScoreCircle,
        data.ats_score.score
    );

    animateScore(
        confidenceCircle,
        Math.round(data.confidence)
    );

}


function animateScore(element,target){

    let current=0;

    target = Math.min(100, Math.max(0, Math.round(Number(target) || 0)));

    if (target === 0) {
        element.textContent = "0%";
        element.style.background =
        `radial-gradient(#1E293B 60%,transparent 61%),
        conic-gradient(
        #EF4444 0deg,
        rgba(255,255,255,.08) 0deg
        )`;
        return;
    }

    const timer=setInterval(()=>{

        current++;

        element.textContent=current+"%";

        let color="#EF4444";

        if(current>=50)
            color="#F59E0B";

        if(current>=75)
            color="#10B981";

        element.style.background=
        `radial-gradient(#1E293B 60%,transparent 61%),
        conic-gradient(
        ${color} ${current*3.6}deg,
        rgba(255,255,255,.08) 0deg
        )`;

        if(current>=target){

            clearInterval(timer);

        }

    },15);

}

/*==========================================================
    CAREER INSIGHTS
==========================================================*/

function updateCareerInsights(data){

    const career=data.career_insights;

    salaryBand.textContent=

        career.salary_band;

    careerLevel.textContent=

        career.career_level;

    interviewReadiness.textContent=

        Math.round(career.interview_readiness)+"%";

    skillsToLearn.innerHTML="";

    career.skills_to_learn.forEach(skill=>{

        const pill=document.createElement("span");

        pill.className="skill-pill";

        pill.textContent=skill;

        skillsToLearn.appendChild(pill);

    });

}

/*==========================================================
    AI SUGGESTIONS
==========================================================*/

function updateSuggestions(data){

    suggestions.innerHTML="";

    data.suggestions.forEach(item=>{

        const div=document.createElement("div");

        div.className="suggestion";

        div.innerHTML=`✅ ${item}`;

        suggestions.appendChild(div);

    });

}

/*==========================================================
    STATISTICS
==========================================================*/

function updateStatistics(data){

    animateNumber(

        skillCount,

        data.analysis.skills.length

    );

    animateNumber(

        educationCount,

        data.analysis.education.length

    );

    animateNumber(

        experienceCount,

        data.recommended_jobs.length

    );

}


function animateNumber(element,target){

    let current=0;

    const timer=setInterval(()=>{

        current++;

        element.textContent=current;

        if(current>=target){

            clearInterval(timer);

        }

    },120);

}

/*==========================================================
    JOBS
==========================================================*/

function updateJobs(data){

    recommendedJobs.innerHTML="";

    data.recommended_jobs.forEach(job=>{

        const card=document.createElement("div");

        card.className="job-card";

        card.innerHTML=`


             <h3>

            💼 ${job.title}

            </h3>

            <div class="match-score">

             ${Math.round(job.match_score)}% Match

              </div>

             <p>

              <strong>Salary</strong>

             <br>

             ${job.salary_band}

            </p>

             <p>

             <strong>Career Growth</strong>

              <br>

              ${job.career_growth}

              </p>

              <p>

              <strong>Recommendation</strong>

              <br>

              ${job.recommendation}

              </p>

              <button class="apply-btn">

              Learn More

              </button>

              `;


        recommendedJobs.appendChild(card);

    });

}
/*==========================================================
    TOAST
==========================================================*/

function showToast(message){

    const toast = document.getElementById("toast");
    const toastMessage = document.getElementById("toastMessage");

    if (!toast || !toastMessage) {

        console.error("Toast elements not found.");

        return;

    }

    toastMessage.textContent = message;

    toast.classList.add("show");

    setTimeout(() => {

        toast.classList.remove("show");

    }, 3000);

}

/*==========================================================
    DOWNLOAD REPORT
==========================================================*/

downloadReport.addEventListener("click", () => {

    if (!responseData) {

        showToast("Analyze a resume first.");

        return;

    }

    const file = responseData.report_file;

    window.open("/download-report/" + file, "_blank");

});

/*==========================================================
    CARD ANIMATION
==========================================================*/

function animateCards(){

    document

    .querySelectorAll(".card,.score-card,.stat-card,.job-card")

    .forEach((card,index)=>{

        card.style.opacity=0;

        card.style.transform="translateY(40px)";

        setTimeout(()=>{

            card.style.transition=".6s";

            card.style.opacity=1;

            card.style.transform="translateY(0)";

        },index*120);

    });

}

/*==========================================================
    THEME
==========================================================*/

const themeToggle=document.getElementById("themeToggle");

themeToggle.addEventListener("click",()=>{

    document.body.classList.toggle("light");

});

/*==========================================================
    SKELETON LOADING
==========================================================*/

function showSkeleton() {

    document.querySelectorAll(

        ".score-card, .card, .job-card, .stat-card"

    ).forEach(card => {

        card.classList.add("skeleton");

    });

}

function hideSkeleton() {

    document.querySelectorAll(

        ".score-card, .card, .job-card, .stat-card"

    ).forEach(card => {

        card.classList.remove("skeleton");

    });

}

/*==========================================================
    RESET DASHBOARD
==========================================================*/

function resetDashboard() {

    dashboard.classList.add("hidden");

    resumePreview.src = "";

    candidateName.textContent = "-";

    candidateEmail.textContent = "-";

    candidatePhone.textContent = "-";

    prediction.textContent = "-";

    resumeScoreCircle.textContent = "0%";

    atsScoreCircle.textContent = "0%";

    confidenceCircle.textContent = "0%";

    recommendedJobs.innerHTML = "";

    suggestions.innerHTML = "";

    skillCount.textContent = "0";

    educationCount.textContent = "0";

    experienceCount.textContent = "0";

}

/*==========================================================
    DOWNLOAD REPORT
==========================================================*/

downloadReport.addEventListener("click", () => {

    console.log("Download button clicked!");

    if (!responseData) {

        showToast("Analyze a resume first.");

        return;

    }

    console.log(responseData);

    window.open(
        "/download-report/" + responseData.report_file,
        "_blank"
    );

});