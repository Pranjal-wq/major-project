package C;

import android.os.Binder;
import android.os.IBinder;
import android.os.IInterface;

/* loaded from: classes.dex */
public interface a extends IInterface {

    /* renamed from: g  reason: collision with root package name */
    public static final String f1212g = "androidx$core$app$unusedapprestrictions$IUnusedAppRestrictionsBackportCallback".replace('$', '.');

    /* renamed from: C.a$a  reason: collision with other inner class name */
    /* loaded from: classes.dex */
    public static abstract class AbstractBinderC0036a extends Binder implements a {

        /* renamed from: C.a$a$a  reason: collision with other inner class name */
        /* loaded from: classes.dex */
        private static class C0037a implements a {

            /* renamed from: a  reason: collision with root package name */
            private IBinder f1213a;

            C0037a(IBinder iBinder) {
                this.f1213a = iBinder;
            }

            @Override // android.os.IInterface
            public IBinder asBinder() {
                return this.f1213a;
            }
        }

        public static a c(IBinder iBinder) {
            if (iBinder == null) {
                return null;
            }
            IInterface queryLocalInterface = iBinder.queryLocalInterface(a.f1212g);
            if (queryLocalInterface != null && (queryLocalInterface instanceof a)) {
                return (a) queryLocalInterface;
            }
            return new C0037a(iBinder);
        }
    }
}