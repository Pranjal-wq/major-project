package H4;

import java.lang.Comparable;
import java.util.Comparator;

/* loaded from: classes2.dex */
public class l<A extends Comparable<A>> implements Comparator<A> {

    /* renamed from: a  reason: collision with root package name */
    private static l f1843a = new l();

    private l() {
    }

    public static <T extends Comparable<T>> l<T> b(Class<T> cls) {
        return f1843a;
    }

    /* renamed from: a */
    public int compare(A a9, A a10) {
        return a9.compareTo(a10);
    }
}