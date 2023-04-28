let count = 1;

function addTest() {
    const question_container = document.getElementById("question_container");

    const question_div = document.createElement("div");
    question_div.className = "question";

    const question_input = document.createElement("input")

    question_input.type = "text";
    question_input.name = "question_" + count++;
    question_div.appendChild(question_input);

    const remove_question = document.createElement("button");
    remove_question.type = "button";
    remove_question.innerHTML = "-";
    remove_question.onclick = function () {
        question_div.remove();
    }

    const add_choice = document.createElement("button");
    add_choice.type = "button";
    add_choice.innerHTML = "Add choice";

    let choice_count = 1;
    add_choice.onclick = function() {
        const choice_div = document.createElement("div");

        const choice_input = document.createElement("input");
        choice_input.type = "text";
        choice_input.name = "choice_" + question_input.name + "_" + choice_count++;

        const remove_choice = document.createElement("button");
        remove_choice.type = "button";
        remove_choice.innerHTML = "-";

        remove_choice.onclick = function () {
            choice_div.remove();
        }

        question_div.appendChild(choice_div)
        choice_div.appendChild(choice_input);
        choice_div.appendChild(remove_choice);
    };
    question_div.appendChild(add_choice);
    question_div.appendChild(remove_question);
    question_container.appendChild(question_div);
}
