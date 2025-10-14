package A5;

import java.util.NoSuchElementException;

/* loaded from: classes2.dex */
public final class g<T> {

    /* renamed from: a  reason: collision with root package name */
    private final T f219a;

    private g() {
        this.f219a = null;
    }

    public static <T> g<T> a() {
        return new g<>();
    }

    public static <T> g<T> b(T t8) {
        if (t8 == null) {
            return a();
        }
        return e(t8);
    }

    public static <T> g<T> e(T t8) {
        return new g<>(t8);
    }

    public T c() {
        T t8 = this.f219a;
        if (t8 != null) {
            return t8;
        }
        throw new NoSuchElementException("No value present");
    }

    public boolean d() {
        if (this.f219a != null) {
            return true;
        }
        return false;
    }

    private g(T t8) {
        if (t8 != null) {
            this.f219a = t8;
            return;
        }
        throw new NullPointerException("value for optional is empty.");
    }
}