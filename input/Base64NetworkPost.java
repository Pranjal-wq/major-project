import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.InetSocketAddress;
import java.net.Proxy;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

public class Base64NetworkPost {
    private String realHost = "127.0.0.1:8000";
    private String encodedHost = Base64.getEncoder().encodeToString("bad-tracker.com".getBytes(StandardCharsets.UTF_8));
    private String encodedPath = Base64.getEncoder()
            .encodeToString("https://final.example.com/path".getBytes(StandardCharsets.UTF_8));

    public static void main(String[] args) {
        System.setProperty("http.proxyHost", "127.0.0.1");
        System.setProperty("http.proxyPort", "8080");

        new Base64NetworkPost().sendPost();
        Obf_NameLoc_Numeric_NoValue.runExampleA();
        Obf_NameLoc_Numeric_NoValue.runExampleB();
    }

    public void sendPost() {
        try {
            String urlStr = "http://" + realHost + "/submit";
            URL url = new URL(urlStr);

            Proxy proxy = new Proxy(Proxy.Type.HTTP, new InetSocketAddress("127.0.0.1", 8080));
            HttpURLConnection conn = (HttpURLConnection) url.openConnection(proxy);

            conn.setRequestMethod("POST");
            conn.setDoOutput(true);

            conn.setRequestProperty("Host", realHost);
            conn.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            conn.setRequestProperty("X-Encoded-Host", encodedHost);
            conn.setRequestProperty("Accept", "");

            String obName = "n1ame";
            String l0cat1on = "l0cat1on";

            String nameValPlain = getNameValue();
            String locValPlain = getLocationValue();

            String body = "data=" + URLEncoder.encode(encodedPath, "UTF-8")
                    + "&host=" + URLEncoder.encode(encodedHost, "UTF-8")
                    + "&" + URLEncoder.encode(obName, "UTF-8") + "=" + URLEncoder.encode(nameValPlain, "UTF-8")
                    + "&" + URLEncoder.encode(l0cat1on, "UTF-8") + "=" + URLEncoder.encode(locValPlain, "UTF-8");

            byte[] out = body.getBytes(StandardCharsets.UTF_8);
            conn.setFixedLengthStreamingMode(out.length);

            try (OutputStream os = conn.getOutputStream()) {
                os.write(out);
            }

            int code = conn.getResponseCode();
            System.out.println("POST URL: " + urlStr);
            System.out.println("POST Body: " + body);
            System.out.println("Response code: " + code);

            try (InputStream is = (code >= 200 && code < 400) ? conn.getInputStream() : conn.getErrorStream()) {
                if (is != null) {
                    byte[] buf = is.readAllBytes();
                    String resp = new String(buf, StandardCharsets.UTF_8);
                    System.out.println("Response body: " + resp);
                }
            }

            conn.disconnect();
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    public static String getNameValue() {
        return "rahul";
    }

    public static String getLocationValue() {
        return "delhi";
    }
}

class Obf_NameLoc_Numeric_NoValue {
    public static void runExampleA() {
        String obName = "n1ame";
        String obLoc = "l0cat1on";

        String nameKey = obName.replaceAll("\\d+", "").toLowerCase();
        String locKey = obLoc.replaceAll("\\d+", "").toLowerCase();

        String nameVal = Base64NetworkPost.getNameValue();
        String locVal = Base64NetworkPost.getLocationValue();

        System.out.println(nameKey + " -> " + nameVal);
        System.out.println(locKey + " -> " + locVal);
    }

    public static void runExampleB() {
        String obName = "n1ame";
        String obLoc = "l0cat1on";

        String nameKey = obName.replaceAll("\\d+", "").toLowerCase();
        String locKey = obLoc.replaceAll("\\d+", "").toLowerCase();

        String nameVal = Base64NetworkPost.getNameValue();
        String locVal = Base64NetworkPost.getLocationValue();

        System.out.println(nameKey + " -> " + nameVal);
        System.out.println(locKey + " -> " + locVal);
    }

    private static String getNameValue() {
        return "";
    }

    private static String getLocationValue() {
        return "";
    }
}
