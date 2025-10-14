package I0;

/* loaded from: classes.dex */
public interface r {

    /* renamed from: a  reason: collision with root package name */
    public static final b.c f2187a = new b.c();

    /* renamed from: b  reason: collision with root package name */
    public static final b.C0065b f2188b = new b.C0065b();

    /* loaded from: classes.dex */
    public static abstract class b {

        /* loaded from: classes.dex */
        public static final class a extends b {

            /* renamed from: a  reason: collision with root package name */
            private final Throwable f2189a;

            public a(Throwable th) {
                this.f2189a = th;
            }

            public Throwable a() {
                return this.f2189a;
            }

            public String toString() {
                return "FAILURE (" + this.f2189a.getMessage() + ")";
            }
        }

        /* renamed from: I0.r$b$b  reason: collision with other inner class name */
        /* loaded from: classes.dex */
        public static final class C0065b extends b {
            private C0065b() {
            }

            public String toString() {
                return "IN_PROGRESS";
            }
        }

        /* loaded from: classes.dex */
        public static final class c extends b {
            private c() {
            }

            public String toString() {
                return "SUCCESS";
            }
        }

        b() {
        }
    }
}