package E2;

import android.os.Build;
import android.util.Log;

/* loaded from: classes.dex */
public final class a {
    private static String a(String str, String str2) {
        String str3 = str + str2;
        if (str3.length() > 23) {
            return str3.substring(0, 23);
        }
        return str3;
    }

    public static void b(String str, String str2, Object obj) {
        String e9 = e(str);
        if (Log.isLoggable(e9, 3)) {
            Log.d(e9, String.format(str2, obj));
        }
    }

    public static void c(String str, String str2, Object... objArr) {
        String e9 = e(str);
        if (Log.isLoggable(e9, 3)) {
            Log.d(e9, String.format(str2, objArr));
        }
    }

    public static void d(String str, String str2, Throwable th) {
        String e9 = e(str);
        if (Log.isLoggable(e9, 6)) {
            Log.e(e9, str2, th);
        }
    }

    private static String e(String str) {
        if (Build.VERSION.SDK_INT < 26) {
            return a("TRuntime.", str);
        }
        return "TRuntime." + str;
    }

    public static void f(String str, String str2, Object obj) {
        String e9 = e(str);
        if (Log.isLoggable(e9, 4)) {
            Log.i(e9, String.format(str2, obj));
        }
    }

    public static void g(String str, String str2, Object obj) {
        String e9 = e(str);
        if (Log.isLoggable(e9, 5)) {
            Log.w(e9, String.format(str2, obj));
        }
    }
}