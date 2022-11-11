import { parse } from "acorn";
import * as fs from "fs";
const analyse = require("analyse-control");

var code = fs.readFileSync('./src/hello.js').toString();

const ast = parse(code, { ecmaVersion: 6 });

// console.log(ast);
const graph = analyse(ast);
let flow = graph.getStartOfFlow();

function flowTraverse(flow) {
  if (flow != undefined) {
    let type = `${flow.getNode().type} `;
    if (flow.isHoist()) {
      type += 'hoist ';
    }
    if (flow.isEnter()) {
      type += 'enter ';
    }
    if (flow.isExit()) {
      type += 'exit ';
    }

    console.log(type, flow.getId(), flow.getNode());
    // if (flow.getNode().type === 'FunctionDeclaration' && flow.isEnter()) {
    //   const bodyAst = graph.getNode(flow.body);
    //   console.log(bodyAst);
    //   const bodyGraph = analyse(bodyAst);
    //   flowTraverse(bodyGraph.getStartOfFlow());
    // }

    flow.getForwardFlows().map(nextFlow => flowTraverse(nextFlow));
  }
}

flowTraverse(flow);