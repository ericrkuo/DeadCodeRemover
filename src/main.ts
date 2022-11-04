import {parse} from "acorn";
import {ancestor} from "acorn-walk";
import {generate} from "astring";

// Sample code to parse
const code = 'let answer = 4 + 7 * 5 + 3;\n'

/**
 * Generate the AST.
 * Library: https://github.com/acornjs/acorn/tree/master/acorn/
 */
const ast = parse(code, { ecmaVersion: 6 })

/**
 * Modify AST by inserting a print statement.
 * The below structure corresponds to the code: console.log("hi the answer is " + answer)
 */
const nodeToInsert = {
    "type": "ExpressionStatement",
    "expression": {
        "type": "CallExpression",
        "callee": {
            "type": "MemberExpression",
            "object": {
                "type": "Identifier",
                "name": "console"
            },
            "property": {
                "type": "Identifier",
                "name": "log"
            },
            "computed": false
        },
        "arguments": [
            {
                "type": "BinaryExpression",
                "left": {
                    "type": "Literal",
                    "value": "hi the answer is ",
                    "raw": "\"hi the answer is \""
                },
                "operator": "+",
                "right": {
                    "type": "Identifier",
                    "name": "answer"
                }
            }
        ]
    }
}

/**
 * Traverse using visitor. The second param declares visitors, and the method name dictates when it gets called.
 * See https://github.com/acornjs/acorn/tree/master/acorn-walk/#interface for more details
 */
ancestor(ast, {
    /**
     * Gets called whenever acorn sees a node with type "VariableDeclaration"
     */
    VariableDeclaration(node: any, ancestors: any){
        // get the parent and insert node
        ancestors[0].body.push(nodeToInsert)
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
