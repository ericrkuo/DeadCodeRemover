// Optionally register instrumentation libraries
import {registerInstrumentations} from "@opentelemetry/instrumentation";
import {Resource} from "@opentelemetry/resources";
import {SemanticResourceAttributes} from "@opentelemetry/semantic-conventions";
import {NodeTracerProvider} from "@opentelemetry/sdk-trace-node";
import {ZipkinExporter} from "@opentelemetry/exporter-zipkin";
import {BatchSpanProcessor, ConsoleSpanExporter, SimpleSpanProcessor} from "@opentelemetry/sdk-trace-base";
import {trace} from "@opentelemetry/api";
import {NodeSDK} from "@opentelemetry/sdk-node";

// https://stackoverflow.com/questions/71654897/opentelemetry-typescript-project-zipkin-exporter
module.exports = (serviceName) => {

    //Specify zipkin url. defualt url is http://localhost:9411/api/v2/spans
    const zipkinUrl = 'http://localhost';
    const zipkinPort = '9411';
    const zipkinPath = '/api/v2/spans';
    const zipkinURL = `${zipkinUrl}:${zipkinPort}${zipkinPath}`;

    const options = {
        headers: {
            'my-header': 'header-value',
        },
        url: zipkinURL,
        //serviceName: 'your-application-name',


        // optional interceptor
        getExportRequestHeaders: () => {
            return {
                'my-header': 'header-value',
            }
        }
    }
    const traceExporter_zipkin = new ZipkinExporter(options);

    const provider = new NodeTracerProvider({
        resource: new Resource({
            [SemanticResourceAttributes.SERVICE_NAME]: serviceName,
        }),
    });

    provider.addSpanProcessor(new SimpleSpanProcessor(new ConsoleSpanExporter()));
    provider.addSpanProcessor(new SimpleSpanProcessor(traceExporter_zipkin));

    provider.register();

    registerInstrumentations({
        instrumentations: [],
    });

    return trace.getTracer(serviceName);
}
// export function init(serviceName: string): NodeTracerProvider {
//     registerInstrumentations({
//         instrumentations: [],
//     });
//
//     const resource =
//         Resource.default().merge(
//             new Resource({
//                 [SemanticResourceAttributes.SERVICE_NAME]: serviceName,
//                 [SemanticResourceAttributes.SERVICE_VERSION]: "0.1.0",
//             })
//         );
//
//     const provider = new NodeTracerProvider({
//         resource: resource,
//     });
//     // const exporter = new ZipkinExporter({serviceName});
//     const exporter = new ConsoleSpanExporter();
//     const processor = new BatchSpanProcessor(exporter);
//     provider.addSpanProcessor(processor);
//
//     provider.register();
//
//     trace.setGlobalTracerProvider(provider)
//
//     const sdk = new NodeSDK({
//         traceExporter: exporter
//     });
//     sdk.start()
//         .then(() => {
//             console.log('Tracing initialized')
//             const tracer = provider.getTracer("default");
//             tracer.startActiveSpan('main', span => {
//                 for (let i = 0; i < 10; i += 1) {
//                     console.log(i)
//                 }
//
//                 // Be sure to end the span!
//                 span.end();
//             });
//         })
//         .catch((error) => console.log('Error initializing tracing', error));
//
//     process.on('SIGTERM', () => {
//         sdk.shutdown()
//             .then(() => console.log('Tracing terminated'))
//             .catch((error) => console.log('Error terminating tracing', error))
//             .finally(() => process.exit(0));
//     });
//
//     return provider;
// }
