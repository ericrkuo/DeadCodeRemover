import {parse} from "acorn";
import {ancestor} from "acorn-walk";
import {generate} from "astring";
// import {init} from "./tracing";
import {trace} from "@opentelemetry/api";

// Initialize tracing

// const provider = init("service-name-here")
const tracer = require('./tracing.ts')('app-services');

// tracer.startActiveSpan('main', span => {
//     for (let i = 0; i < 10; i += 1) {
//         console.log(i)
//     }
//
//     // Be sure to end the span!
//     span.end();
// });

// Sample code to parse
let  code = `let answer = 4 + 7 * 5 + 3;\n`

code = `
var x = 1;
x+=1;
console.log(x);
`
// const code = `const span = tracer.startSpan('test');
// span.end();
// `;

// const code = `
// tracer.startActiveSpan('main', span => {
//     span.end();
// });
// `;

/**
 * Generate the AST.
 * Library: https://github.com/acornjs/acorn/tree/master/acorn/
 */
const ast = parse(code, { ecmaVersion: 6 })

/**
 * Modify AST by inserting a print statement.
 * The below structure corresponds to the code: console.log("hi the answer is " + answer)
 */
const spanStart = {
    "type": "VariableDeclaration",
    "declarations": [
        {
            "type": "VariableDeclarator",
            "id": {
                "type": "Identifier",
                "name": "span"
            },
            "init": {
                "type": "CallExpression",
                "callee": {
                    "type": "MemberExpression",
                    "object": {
                        "type": "Identifier",
                        "name": "tracer"
                    },
                    "property": {
                        "type": "Identifier",
                        "name": "startSpan"
                    },
                    "computed": false
                },
                "arguments": [
                    {
                        "type": "Literal",
                        "value": "test",
                        "raw": "'test'"
                    }
                ]
            }
        }
    ],
    "kind": "const"
}

const spanEnd = {
    "type": "ExpressionStatement",
    "expression": {
        "type": "CallExpression",
        "callee": {
            "type": "MemberExpression",
            "object": {
                "type": "Identifier",
                "name": "span"
            },
            "property": {
                "type": "Identifier",
                "name": "end"
            },
            "computed": false
        },
        "arguments": []
    }
}

let added = false
/**
 * Traverse using visitor. The second param declares visitors, and the method name dictates when it gets called.
 * See https://github.com/acornjs/acorn/tree/master/acorn-walk/#interface for more details
 */
ancestor(ast, {
    /**
     * Gets called whenever acorn sees a node with type "VariableDeclaration"
     */
    VariableDeclaration(node: any, ancestors: any) {
        // get the parent and insert node
        if (!added) {
            ancestors[0].body.unshift(spanStart)
            ancestors[0].body.push(spanEnd)
            added = true
        }
    }
})

/**
 * Format the AST back to code
 * Library: https://github.com/davidbonnet/astring
 */
const formattedCode = generate(ast)

/**
 * Execute the code
 */
eval(formattedCode)
