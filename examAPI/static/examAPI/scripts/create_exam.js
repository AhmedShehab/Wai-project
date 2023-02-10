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
	var chapters_container = document.getElementById("chapters-container");
	var selected_course = self.options[self.selectedIndex].value;
	chapters_container.innerHTML = "";
	fetch(`/chapter/?course=${selected_course}`, {
		method: "GET"
	})
		.then(response => response.json())
		.then(data => {
			data.forEach(element => {
				// Create a div that holds the label and input field of every chapter
				var chapter_instance = create_label_input_container(element);
				// Add the input field to every chapter
				var chapter_input = create_input_fields(element);
				// Append the label and input fields in chapter instance
				var chapter_label = create_label_field(element);
				// Then append the chapter instance in the all chapters container
				chapter_instance.append(chapter_label);
				chapter_input.forEach(input => {
					input.type = "number";
					input.min = "0";
					input.required = true;
					chapter_instance.append(input);
				});
				chapters_container.append(chapter_instance);
			});
		});
}
function create_input_fields(element) {
	// Number of questions input field
	var chapter_questions_input = document.createElement("input");
	chapter_questions_input.className = `form-control chapter-questions`;
	chapter_questions_input.name = "chapter-questions";
	chapter_questions_input.max = "12";
	chapter_questions_input.placeholder = "No. of Questions";
	// Number of easy questions input
	var chapter_easy_input = document.createElement("input");
	chapter_easy_input.className = `form-control chapter-easy`;
	chapter_easy_input.name = "easy-questions";
	chapter_easy_input.placeholder = "No. Easy Questions";
	// Number of difficult questions input
	var chapter_difficult_input = document.createElement("input");
	chapter_difficult_input.className = `form-control chapter-difficult`;
	chapter_difficult_input.name = "difficult-questions";
	chapter_difficult_input.placeholder = "No. Difficult Questions";
	// Number of reminding questions input
	var chapter_reminding_input = document.createElement("input");
	chapter_reminding_input.className = `form-control chapter-reminding`;
	chapter_reminding_input.name = "reminding-questions";
	chapter_reminding_input.placeholder = "No. Reminding Questions";
	// Number of understanding questions
	var chapter_understanding_input = document.createElement("input");
	chapter_understanding_input.className = `form-control chapter-understanding`;
	chapter_understanding_input.name = "understanding-questions";
	chapter_understanding_input.placeholder = "No. Understanding Questions";
	// Number of creativity questions
	var chapter_creativity_input = document.createElement("input");
	chapter_creativity_input.className = `form-control chapter-creativity`;
	chapter_creativity_input.name = "creativity-questions";
	chapter_creativity_input.placeholder = "No. Creativity Questions";

	var chapter_input = [
		chapter_questions_input,
		chapter_easy_input,
		chapter_difficult_input,
		chapter_reminding_input,
		chapter_understanding_input,
		chapter_creativity_input
	];
	return chapter_input;
}
function create_label_field(element) {
	var chapter_label = document.createElement("label");
	chapter_label.className = "form-label";
	chapter_label.innerText = `${element.name}`;
	return chapter_label;
}
function create_label_input_container(element) {
	var chapter_instance = document.createElement("div");
	chapter_instance.className = "chapter-div";
	chapter_instance.dataset["id"] = `${element.id}`;
	chapter_instance.style.display = "flex";
	chapter_instance.style.flexDirection = "column";
	return chapter_instance;
}

function get_exammetadata() {
	var chapters = document.getElementsByClassName("chapter-div");
	var metadata = [];
	Array.from(chapters).forEach(item => {
		const chapter = item.dataset["id"];
		const questions = item.querySelector(
			'[name="chapter-questions"]'
		).value;
		const easy = item.querySelector('[name="easy-questions"]').value;
		const difficult = item.querySelector('[name="difficult-questions"]').value;
		const reminding = item.querySelector(
			'[name="reminding-questions"]'
		).value;
		const understanding = item.querySelector(
			'[name="understanding-questions"]'
		).value;
		const creativity = item.querySelector(
			'[name="creativity-questions"]'
		).value;
		metadata.push({
			chapter: chapter,
			no_of_questions: questions,
			no_of_easy_questions: easy,
			no_of_difficult_questions: difficult,
			no_of_reminding_questions: reminding,
			no_of_understanding_questions: understanding,
			no_of_creativity_questions: creativity
		});
	});
	return metadata;
}
function generateExam() {
	var course_options = document.getElementById("course-options");
	var selected_course =
		course_options.options[course_options.selectedIndex].value;
	var form = document.getElementById("exam-form");
	var csrftoken = form.getElementsByTagName("input")[0].value;
	var metadata = get_exammetadata();
	post_exam(metadata, selected_course, csrftoken);
	
}
function post_exam(metadata, course, csrftoken) {
	fetch(`/exam/`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"X-CSRFToken": csrftoken
		},
		body: JSON.stringify({
			course: course,
			metadata: metadata
		})
	})
		.then(response => response.json())
		.then(data => {
			location.href=`http://127.0.0.1:8000/exam_instance/${data['id']}`;
		});
}
