# Miniproject
#hii chinmayee here
#hii miniproject presentation here very frustated
#  <script>
        function updateCounter(textarea, counterId) {
            let maxLength = 1000;
            let remaining = maxLength - textarea.value.length;
            document.getElementById(counterId).textContent = remaining + " characters remaining";
        }
    
        function generateTeamFields() {
            let count = document.getElementById('team-count').value;
            let container = document.getElementById('team-members');
            container.innerHTML = ""; // Clear previous inputs
    
            for (let i = 1; i <= count; i++) {
                let div = document.createElement("div");
                div.classList.add("form-group");
                div.innerHTML = `
                    <label>Team Member ${i} Name:</label>
                    <input type="text" name="team_member_${i}_name" required>
                    <label>Team Member ${i} Email:</label>
                    <input type="email" name="team_member_${i}_email" required>
                `;
                container.appendChild(div);
            }
        }
    
        function populateAcademicYears() {
            const dropdown = document.getElementById('academic_year');
            dropdown.innerHTML = '<option value="" disabled selected>Select Academic Year</option>';
    
            const currentYear = new Date().getFullYear();
            const startYear = 2019;
    
            for (let year = currentYear; year >= startYear; year--) {
                const nextYear = year + 1;
                const option = document.createElement('option');
                option.value = `${year}-${nextYear}`;
                option.textContent = `${year}-${nextYear}`;
                dropdown.appendChild(option);
            }
        }
    
        document.addEventListener('DOMContentLoaded', populateAcademicYears);
    </script>

    #{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Idea Submission</title>
    <style>
        body {
            background: linear-gradient(to bottom, #FFA500, #FFFFFF);
            font-family: Arial, sans-serif;
            padding: 20px;
        }
        .container {
            width: 50%; /* Reduced form width */
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
        }
        h1 {
            background: #ff6680;
            color: white;
            padding: 15px;
            text-align: center;
            border-radius: 10px;
            font-size: 24px;
            font-weight: bold;
        }
        .form-group {
            margin: 15px 0;
        }
        label {
            font-weight: bold;
            display: block;
            margin-bottom: 5px;
            font-size: 18px; /* Increased size */
        }
        input, textarea, select {
            width: 100%; /* Standardized width */
            height: 45px; /* Standardized height */
            padding: 12px;
            margin-top: 5px;
            border-radius: 5px;
            border: 1px solid #ccc;
            font-size: 18px; /* Increased size */
            
            box-sizing: border-box;
        }
        textarea {
            height: 120px; /* Adjusted for text areas */
        }
        .btn {
            background: #ff6680;
            color: white;
            border: none;
            padding: 14px;
            border-radius: 5px;
            cursor: pointer;
            display: block;
            width: 100%; /* Matching input field width */
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            margin: auto;
        }
        .btn:hover {
            background: #ff3355;
        }
        .char-counter {
            text-align: right;
            font-size: 14px;
            color: gray;
            margin-top: 3px;
            font-weight: bold;
        }
    </style>
      <script>
        function updateCounter(textarea, counterId) {
            let maxLength = 1000;
            let remaining = maxLength - textarea.value.length;
            document.getElementById(counterId).textContent = remaining + " characters remaining";
        }

        function generateTeamFields() {
            let count = document.getElementById('team-count').value;
            let container = document.getElementById('team-members');
            container.innerHTML = "";

            for (let i = 1; i <= count; i++) {
                let div = document.createElement("div");
                div.classList.add("form-group");
                div.innerHTML = `
                    <label>Team Member ${i} Name:</label>
                    <input type="text" name="team_member_${i}_name" required>
                    <label>Team Member ${i} Email:</label>
                    <input type="email" name="team_member_${i}_email" required>
                `;
                container.appendChild(div);
            }
        }

        function populateAcademicYears() {
            const dropdown = document.getElementById('academic_year');
            dropdown.innerHTML = '<option value="" disabled selected>Select Academic Year</option>';
            const currentYear = new Date().getFullYear();
            const startYear = 2019;
            for (let year = currentYear; year >= startYear; year--) {
                const nextYear = year + 1;
                const option = document.createElement('option');
                option.value = `${year}-${nextYear}`;
                option.textContent = `${year}-${nextYear}`;
                dropdown.appendChild(option);
            }
        }
        document.addEventListener('DOMContentLoaded', populateAcademicYears);
    </script>
</head>
<body>
    <div class="container">
        <h1>Select and Add Idea and Innovation</h1>

        <div class="form-group">
            <label>Develop as part of</label>
            <select name="develop_as_part" required>
                <option value="">Select an Option</option>
                <option value="academic_requirement">Academic Requirement/Study Project</option>
                <option value="academic_research">Academic Research Assignment/Industry Sponsored Project</option>
                <option value="independent_assignment">Independent Assignment/Non-academic Study Project</option>
            </select>
        </div>

        <div class="form-group">
            <label>Title of Project</label>
            <input type="text" name="title" required>
        </div>

        <div class="form-group">
            <label>Academic Year</label>
            <select id="academic_year" name="academic_year" required>
                <option value="" disabled selected>Select Academic Year</option>
                <option value="2024-2025">2024-2025</option>
                <option value="2023-2024">2023-2024</option>
                <option value="2022-2023">2022-2023</option>
                <option value="2021-2022">2021-2022</option>
                <option value="2020-2021">2020-2021</option>
                <option value="2019-2020">2019-2020</option>
            </select>
        </div>
        

        <!-- Branch Dropdown -->
        <div class="form-group">
            <label for="branch">Branch<span>*</span></label>
            <select name="branch" id="branch" required>
                <option value="" disabled selected>Select your branch</option>
                <option value="Artificial Intelligence & Data Science (AIDS)">Artificial Intelligence & Data Science (AIDS)</option>
                <option value="Artificial Intelligence & Machine Learning (AIML)">Artificial Intelligence & Machine Learning (AIML)</option>
                <option value="Civil Engineering">Civil Engineering</option>
                <option value="Computer Engineering">Computer Engineering</option>
                <option value="Information Technology">Information Technology</option>
                <option value="Internet of Things (IoT)">Internet of Things (IoT)</option>
                <option value="Mechanical Engineering">Mechanical Engineering</option>
            </select>
        </div>

        <div class="form-group">
            <label for="domain">Domain</label>
            <select id="domain" name="domain" required>
                <option value="">Select a Domain</option>
                <option value="IOT">IoT</option>
                <option value="website">Website</option>
                <option value="app">App Development</option>
                <option value="aiml">AI/ML</option>
                <option value="aids">AIDS (Artificial Intelligence & Data Science)</option>
            </select>
        </div>

        <div class="form-group">
            <label>Innovation Type</label>
            <input type="text" name="innovation_type" required>
        </div>

        <div class="form-group">
            <label>Status Level</label>
            <div style="display: flex; gap: 40px; align-items: center;">
                <label style="display: flex; align-items: center; gap: 10px;">
                    <input type="radio" name="status_level" value="1" required> 1
                </label>
                <label style="display: flex; align-items: center; gap: 10px;">
                    <input type="radio" name="status_level" value="2"> 2
                </label>
                <label style="display: flex; align-items: center; gap: 10px;">
                    <input type="radio" name="status_level" value="3"> 3
                </label>
            </div>
        </div>

        <div class="form-group">
            <label>Define the Problem</label>
            <textarea name="problem" rows="3" maxlength="1000" oninput="updateCounter(this, 'problem-counter')" required></textarea>
            <div id="problem-counter" class="char-counter">1000 characters remaining</div>
        </div>

        <div class="form-group">
            <label>Describe the Solution</label>
            <textarea name="solution" rows="3" maxlength="1000" oninput="updateCounter(this, 'solution-counter')" required></textarea>
            <div id="solution-counter" class="char-counter">1000 characters remaining</div>
        </div>

        <div class="form-group">
            <label>Unique Features</label>
            <textarea name="features" rows="3" maxlength="1000" oninput="updateCounter(this, 'features-counter')" required></textarea>
            <div id="features-counter" class="char-counter">1000 characters remaining</div>
        </div>

        <div class="form-group">
            <label>How is it Different?</label>
            <textarea name="difference" rows="3" maxlength="1000" oninput="updateCounter(this, 'difference-counter')" required></textarea>
            <div id="difference-counter" class="char-counter">1000 characters remaining</div>
        </div>

        <div class="form-group">
            <label>Video URL</label>
            <input type="url" name="video_url">
        </div>

        <div class="form-group">
            <label>Upload Photograph (JPG, PNG, PDF max 2MB)</label>
            <input type="file" name="upload" accept=".jpg, .png, .pdf">
        </div>

        <div class="form-group">
            <label>Mentor Name</label>
            <input type="text" name="mentor" required>
        </div>

        <div class="form-group">
            <label>Team Leader Name</label>
            <input type="text" name="team_leader_name" required>
        </div>

        <div class="form-group">
            <label>Team Leader Email</label>
            <input type="email" name="team_leader_email" required>
        </div>

        <div class="form-group">
            <label>Number of Team Members</label>
            <input type="number" id="team-count" name="team_count" min="1" max="10" required onchange="generateTeamFields()">
        </div>

        <div id="team-members"></div>

        <button class="btn">Save and Next</button>
    </div>
   # <script>
        function updateCounter(textarea, counterId) {
            let maxLength = 1000;
            let remaining = maxLength - textarea.value.length;
            document.getElementById(counterId).textContent = remaining + " characters remaining";
        }
    
        function generateTeamFields() {
            let count = document.getElementById('team-count').value;
            let container = document.getElementById('team-members');
            container.innerHTML = ""; // Clear previous inputs
    
            for (let i = 1; i <= count; i++) {
                let div = document.createElement("div");
                div.classList.add("form-group");
                div.innerHTML = `
                    <label>Team Member ${i} Name:</label>
                    <input type="text" name="team_member_${i}_name" required>
                    <label>Team Member ${i} Email:</label>
                    <input type="email" name="team_member_${i}_email" required>
                `;
                container.appendChild(div);
            }
        }
    
        function populateAcademicYears() {
            const dropdown = document.getElementById('academic_year');
            dropdown.innerHTML = '<option value="" disabled selected>Select Academic Year</option>';
    
            const currentYear = new Date().getFullYear();
            const startYear = 2019;
            for (let i = 0; i < 5; i++) { // Show only the last 4 years
        const year = currentYear - i;
        const nextYear = year + 1;
        const option = document.createElement('option');
        option.value = `${year}-${nextYear}`;
        option.textContent = `${year}-${nextYear}`;
        dropdown.appendChild(option);
            }
        }
    
        document.addEventListener('DOMContentLoaded', populateAcademicYears);
    </script>
</body>
</html>#

