package A5;

import android.os.Parcel;
import android.os.Parcelable;
import android.os.SystemClock;
import java.util.concurrent.TimeUnit;

/* loaded from: classes2.dex */
public class l implements Parcelable {
    public static final Parcelable.Creator<l> CREATOR = new a();

    /* renamed from: a  reason: collision with root package name */
    private long f236a;

    /* renamed from: b  reason: collision with root package name */
    private long f237b;

    /* loaded from: classes2.dex */
    class a implements Parcelable.Creator<l> {
        a() {
        }

        /* renamed from: a */
        public l createFromParcel(Parcel parcel) {
            return new l(parcel, (a) null);
        }

        /* renamed from: b */
        public l[] newArray(int i9) {
            return new l[i9];
        }
    }

    public l() {
        this(h(), a());
    }

    private static long a() {
        return TimeUnit.NANOSECONDS.toMicros(SystemClock.elapsedRealtimeNanos());
    }

    public static l f(long j9) {
        long micros = TimeUnit.MILLISECONDS.toMicros(j9);
        return new l(h() + (micros - a()), micros);
    }

    private static long h() {
        return TimeUnit.MILLISECONDS.toMicros(System.currentTimeMillis());
    }

    public long b() {
        return this.f236a + c();
    }

    public long c() {
        return d(new l());
    }

    public long d(l lVar) {
        return lVar.f237b - this.f237b;
    }

    @Override // android.os.Parcelable
    public int describeContents() {
        return 0;
    }

    public long e() {
        return this.f236a;
    }

    public void g() {
        this.f236a = h();
        this.f237b = a();
    }

    @Override // android.os.Parcelable
    public void writeToParcel(Parcel parcel, int i9) {
        parcel.writeLong(this.f236a);
        parcel.writeLong(this.f237b);
    }

    l(long j9, long j10) {
        this.f236a = j9;
        this.f237b = j10;
    }

    private l(Parcel parcel) {
        this(parcel.readLong(), parcel.readLong());
    }

    /* synthetic */ l(Parcel parcel, a aVar) {
        this(parcel);
    }
}