let count = 1;

function addTest() {
    const question_container = document.getElementById("question_container");
    const question_div = document.createElement("div");
    question_div.className = "question";
    const question_input = document.createElement("input");
    question_input.type = "text";
    question_input.name = "question_" + count;
    question_input.placeholder = "Question " + count++;
    question_div.appendChild(question_input);
    const add_choice = document.createElement("button");
    add_choice.type = "button";
    add_choice.innerHTML = "Add choice";
    let choice_count = 1;
    add_choice.onclick = function() {
        const choice_div = document.createElement("div");
        const choice_input = document.createElement("input");
        choice_input.type = "text";
        choice_input.name = "choice_" + question_input.name + "_" + choice_count;
        choice_input.placeholder = "Choice " + choice_count++;
        choice_div.appendChild(choice_input);
        question_div.appendChild(choice_div)
    };
    question_div.appendChild(add_choice);
    question_container.appendChild(question_div);
}
