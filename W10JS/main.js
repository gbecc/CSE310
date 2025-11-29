// simple in-memory list of tasks
let tasks = [];

// grab the elements once so we can reuse them
const taskInput = document.getElementById("task-input");
const addTaskBtn = document.getElementById("add-task-btn");
const taskList = document.getElementById("task-list");
const taskStats = document.getElementById("task-stats");

const countInput = document.getElementById("count-input");
const countBtn = document.getElementById("count-btn");
const countResult = document.getElementById("count-result");
const countError = document.getElementById("count-error");

// **task list code

function addTask() {
  const text = taskInput.value.trim();

  // if the user didn't actually type anything
  if (!text) {
    return;
  }

  const newTask = {
    id: Date.now(),           // quick id
    text: text,
    done: false,
    createdAt: new Date(),    // will pretty-print this with dayjs
  };

  tasks.push(newTask);

  // show updated list on screen
  renderTasks();

  // reset input for the next task
  taskInput.value = "";
  taskInput.focus();
}

function toggleTask(id) {
  // find the matching task and flip the "done" flag
  const task = tasks.find(t => t.id === id);
  if (task) {
    task.done = !task.done;
    renderTasks();
  }
}

function deleteTask(id) {
  // filter out the one we want to remove
  tasks = tasks.filter(t => t.id !== id);
  renderTasks();
}

function renderTasks() {
  // turn the list of tasks into a chunk of html
  taskList.innerHTML = tasks
    .map(task => {
      const timeLabel = dayjs(task.createdAt).format("HH:mm:ss"); // third-party lib
      const itemClass = task.done ? "task-item done" : "task-item";

      return `
        <li class="${itemClass}">
          <div class="task-left">
            <span class="task-text">${task.text}</span>
            <span class="small">added at ${timeLabel}</span>
          </div>
          <div>
            <button onclick="toggleTask(${task.id})">
              ${task.done ? "undo" : "done"}
            </button>
            <button onclick="deleteTask(${task.id})">
              delete
            </button>
          </div>
        </li>
      `;
    })
    .join("");

  // basic stats using array functions
  const total = tasks.length;
  const doneCount = tasks.filter(t => t.done).length;

  taskStats.textContent = `total: ${total} | done: ${doneCount}`;
}

// wire up the buttons / enter key for tasks
addTaskBtn.addEventListener("click", addTask);

taskInput.addEventListener("keyup", (event) => {
  if (event.key === "Enter") {
    addTask();
  }
});

// **recursive countdown code

// straight recursive countdown that returns an array of steps
function buildCountdown(n) {
  if (n <= 0) {
    return ["liftoff!"];
  }

  // take the current number and then whatever comes next
  const rest = buildCountdown(n - 1);
  return [n, ...rest];
}

function runCountdown() {
  const raw = countInput.value;
  const num = Number(raw);

  // clear old messages
  countResult.textContent = "";
  countError.textContent = "";

  try {
    // if the value isn't a positive whole number, blow up on purpose
    if (!Number.isInteger(num) || num <= 0) {
      throw new Error("please type a positive whole number (1, 2, 3, ...)");
    }

    const steps = buildCountdown(num);
    countResult.textContent = steps.join(" → ");
  } catch (err) {
    // this is the stretch challenge: actually catching the error
    countError.textContent = err.message;
  }
}

// hook up countdown button
countBtn.addEventListener("click", runCountdown);
