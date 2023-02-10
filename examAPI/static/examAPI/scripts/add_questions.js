fetch("/course/", {
	method: "GET"
})
	.then(response => response.json())
	.then(data => {
		data.forEach(element => {
			course_select_field = document.getElementById("course-options");
			var option = document.createElement("option");
			option.text = `${element.name}`;
			option.name = `${element.name}`;
			option.value = `${element.id}`;
			course_select_field.add(option);
		});
	});
function getChapters(self) {
	var chapter_select_feild = document.getElementById("chapter-options");
	document.getElementById("questions-container").style.display = "none";
	document.getElementById("questions-container").disabled = true;
	chapter_select_feild.innerHTML = `<option value="" disabled selected>Select Chapter</option>`;
	var selected_course = self.options[self.selectedIndex].value;
	fetch(`/chapter/?course=${selected_course}`, {
		method: "GET"
	})
		.then(response => response.json())
		.then(data => {
			data.forEach(element => {
				course_select_field = document.getElementById("chapter-options");
				var option = document.createElement("option");
				option.text = `${element.name}`;
				option.name = `${element.name}`;
				option.value = `${element.id}`;
				course_select_field.add(option);
			});
		});
}
function show_questions() {
	document.getElementById("questions-container").style.display = "flex";
	document.getElementById("questions-container").style.flexWrap = "nowrap";
	document.getElementById("questions-container").style.justifyContent = "space-evenly";
}
function submit_questions(form) {
	try {
		var chapter = document.getElementById("chapter-options");
		var selected_chapter = chapter.options[chapter.selectedIndex].value;
		var easy_questions = document.getElementById("easy-questions");
		var difficult_questions = document.getElementById("difficult-questions");
		var csrftoken = form.getElementsByTagName("input")[0].value;
		post_question_data("easy", easy_questions,csrftoken,selected_chapter);
		post_question_data("difficult", difficult_questions,csrftoken,selected_chapter);
		location.href ='http://127.0.0.1:8000/'
	} catch (error) {
		console.log(error);
	}
}

function post_question_data(difficulty, questions,csrftoken,chapter) {
	for (div of questions.querySelectorAll("div")) {
		var objective = div.dataset["objective"];
		const content = div.querySelector('[name="content"]').value;
		const wrong1 = div.querySelector('[name="wrongAnswer1"]').value;
		const wrong2 = div.querySelector('[name="wrongAnswer2"]').value;
		const right = div.querySelector('[name="rightAnswer"]').value;
		fetch(`/question/`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": csrftoken
			},
			body: JSON.stringify({
				difficulty: difficulty,
				objective: objective,
				content: content,
				wrongAnswer1: wrong1,
				wrongAnswer2: wrong2,
				rightAnswer: right,
				chapter: chapter
			})
		})
			.then(response => response.json())
			.then(data => console.log(data));
	}
}
