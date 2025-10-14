package A5;

/* JADX WARN: Failed to restore enum class, 'enum' modifier removed */
/* loaded from: classes2.dex */
public abstract class k extends Enum<k> {

    /* renamed from: b  reason: collision with root package name */
    public static final k f229b = new a("TERABYTES", 0, 1099511627776L);

    /* renamed from: c  reason: collision with root package name */
    public static final k f230c = new k("GIGABYTES", 1, 1073741824) { // from class: A5.k.b
    };

    /* renamed from: d  reason: collision with root package name */
    public static final k f231d = new k("MEGABYTES", 2, 1048576) { // from class: A5.k.c
    };

    /* renamed from: e  reason: collision with root package name */
    public static final k f232e = new k("KILOBYTES", 3, 1024) { // from class: A5.k.d
    };

    /* renamed from: f  reason: collision with root package name */
    public static final k f233f = new k("BYTES", 4, 1) { // from class: A5.k.e
    };

    /* renamed from: m  reason: collision with root package name */
    private static final /* synthetic */ k[] f234m = b();

    /* renamed from: a  reason: collision with root package name */
    long f235a;

    /* JADX WARN: Failed to restore enum class, 'enum' modifier removed */
    /* loaded from: classes2.dex */
    final class a extends k {
        a(String str, int i9, long j9) {
            super(str, i9, j9, null);
        }
    }

    private k(String str, int i9, long j9) {
        this.f235a = j9;
    }

    private static /* synthetic */ k[] b() {
        return new k[]{f229b, f230c, f231d, f232e, f233f};
    }

    public static k valueOf(String str) {
        return (k) Enum.valueOf(k.class, str);
    }

    public static k[] values() {
        return (k[]) f234m.clone();
    }

    public long d(long j9) {
        return (j9 * this.f235a) / f232e.f235a;
    }

    /* synthetic */ k(String str, int i9, long j9, a aVar) {
        this(str, i9, j9);
    }
}