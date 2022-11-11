function trueFunc() {
  console.log('this is true');
}
function falseFunc() {
  console.log('this is false');
}

const message = "Hello World!";
console.log(message);

const x = "true"
if (x === "true") {
  trueFunc();
} else {
  falseFunc();
}