import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * Offline Java HTTP demo for OCI/Kubernetes/OpenShift design patterns.
 * This is NOT a payment engine or servlet container for EAR/WAR files.
 */
public final class ExampleServer {
    private static final AtomicBoolean READY = new AtomicBoolean(false);

    private static void respond(HttpExchange exchange, int status, String body) throws IOException {
        byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=utf-8");
        exchange.getResponseHeaders().set("Cache-Control", "no-store");
        exchange.sendResponseHeaders(status, bytes.length);
        try (var stream = exchange.getResponseBody()) {
            stream.write(bytes);
        }
    }

    private static String escapeJson(String input) {
        return input.replace("\\", "\\\\").replace("\"", "\\\"")
                    .replace("\n", "\\n").replace("\r", "\\r");
    }

    private static void onlyGet(HttpExchange exchange, int status, String body) throws IOException {
        if (!"GET".equals(exchange.getRequestMethod())) {
            respond(exchange, 405, "{\"error\":\"METHOD_NOT_ALLOWED\"}");
            return;
        }
        respond(exchange, status, body);
    }

    public static void main(String[] args) throws Exception {
        String portValue = System.getenv().getOrDefault("PORT", "8080");
        int port = Integer.parseInt(portValue);
        String mode = System.getenv().getOrDefault("APP_MODE", "demo");
        HttpServer server = HttpServer.create(new InetSocketAddress("0.0.0.0", port), 128);
        ExecutorService pool = Executors.newFixedThreadPool(8);
        server.setExecutor(pool);
        server.createContext("/health/startup", e -> onlyGet(e, 200, "{\"startup\":true}"));
        server.createContext("/health/live", e -> onlyGet(e, 200, "{\"alive\":true}"));
        server.createContext("/health/ready", e -> onlyGet(e, READY.get() ? 200 : 503,
                "{\"ready\":" + READY.get() + "}"));
        server.createContext("/api/status", e -> onlyGet(e, 200,
                "{\"service\":\"java-modernization-demo\",\"status\":\"OK\",\"mode\":\""
                + escapeJson(mode) + "\"}"));
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            READY.set(false);
            System.out.println(Instant.now() + " graceful-shutdown started");
            server.stop(1);
            pool.shutdown();
            try {
                if (!pool.awaitTermination(20, TimeUnit.SECONDS)) {
                    pool.shutdownNow();
                }
            } catch (InterruptedException ignored) {
                pool.shutdownNow();
                Thread.currentThread().interrupt();
            }
            System.out.println(Instant.now() + " graceful-shutdown complete");
        }));
        server.start();
        READY.set(true);
        System.out.println(Instant.now() + " HTTP Java service started on port " + port);
    }
}
