import {parse} from "acorn";
import {ancestor} from "acorn-walk";
import {generate} from "astring";
// import {init} from "./tracing";
import {context, trace} from "@opentelemetry/api";

// Initialize tracing
const tracer = require('./tracing.ts')('app-services');

const programSpan = tracer.startSpan("tracing-demo");
let ctx = trace.setSpan(context.active(), programSpan);

function foo(x: boolean) {
    const span = tracer.startSpan("foo", undefined, ctx);
    ctx = trace.setSpan(context.active(), span);
    if (x) {
        const span1 = tracer.startSpan("A", undefined, ctx);
        span1.setAttribute('IF-CONDITION', true)
        A();
        span1.end();
    } else {
        const span1 = tracer.startSpan("B", undefined, ctx);
        span1.setAttribute('IF-CONDITION', false)
        B();
        span1.end();
    }
    span.end();
}

let A = () => console.log("A");
let B = () => console.log("B");

foo(true);
foo(false);

programSpan.end();

/**
 * Could instrument the code to do this instead:
 * 
 * tracer.startActiveSpan('main', span => {
 *     <INSERT ACTUAL CODE HERE>
 *
 *     span.end();
 * });
 */
