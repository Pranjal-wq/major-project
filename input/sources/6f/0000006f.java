package G7;

/* loaded from: classes3.dex */
public final class c {
    private static final int a(int i9, int i10, int i11) {
        return e(e(i9, i11) - e(i10, i11), i11);
    }

    private static final long b(long j9, long j10, long j11) {
        return f(f(j9, j11) - f(j10, j11), j11);
    }

    public static final int c(int i9, int i10, int i11) {
        if (i11 > 0) {
            if (i9 < i10) {
                return i10 - a(i10, i9, i11);
            }
            return i10;
        } else if (i11 < 0) {
            if (i9 > i10) {
                return i10 + a(i9, i10, -i11);
            }
            return i10;
        } else {
            throw new IllegalArgumentException("Step is zero.");
        }
    }

    public static final long d(long j9, long j10, long j11) {
        int i9 = (j11 > 0L ? 1 : (j11 == 0L ? 0 : -1));
        if (i9 > 0) {
            if (j9 < j10) {
                return j10 - b(j10, j9, j11);
            }
            return j10;
        } else if (i9 < 0) {
            if (j9 > j10) {
                return j10 + b(j9, j10, -j11);
            }
            return j10;
        } else {
            throw new IllegalArgumentException("Step is zero.");
        }
    }

    private static final int e(int i9, int i10) {
        int i11 = i9 % i10;
        if (i11 < 0) {
            return i11 + i10;
        }
        return i11;
    }

    private static final long f(long j9, long j10) {
        long j11 = j9 % j10;
        if (j11 < 0) {
            return j11 + j10;
        }
        return j11;
    }
}