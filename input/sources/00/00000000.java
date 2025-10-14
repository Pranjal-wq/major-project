package C0;

import android.annotation.SuppressLint;
import android.util.Log;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.channels.FileChannel;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
import kotlin.jvm.internal.g;
import kotlin.jvm.internal.m;

/* loaded from: classes.dex */
public final class a {

    /* renamed from: e  reason: collision with root package name */
    public static final C0038a f1215e = new C0038a(null);

    /* renamed from: f  reason: collision with root package name */
    private static final Map<String, Lock> f1216f = new HashMap();

    /* renamed from: a  reason: collision with root package name */
    private final boolean f1217a;

    /* renamed from: b  reason: collision with root package name */
    private final File f1218b;
    @SuppressLint({"SyntheticAccessor"})

    /* renamed from: c  reason: collision with root package name */
    private final Lock f1219c;

    /* renamed from: d  reason: collision with root package name */
    private FileChannel f1220d;

    /* renamed from: C0.a$a  reason: collision with other inner class name */
    /* loaded from: classes.dex */
    public static final class C0038a {
        private C0038a() {
        }

        /* JADX INFO: Access modifiers changed from: private */
        public final Lock b(String str) {
            Lock lock;
            synchronized (a.f1216f) {
                try {
                    Map map = a.f1216f;
                    Object obj = map.get(str);
                    if (obj == null) {
                        obj = new ReentrantLock();
                        map.put(str, obj);
                    }
                    lock = (Lock) obj;
                } catch (Throwable th) {
                    throw th;
                }
            }
            return lock;
        }

        public /* synthetic */ C0038a(g gVar) {
            this();
        }
    }

    public a(String name, File lockDir, boolean z8) {
        m.f(name, "name");
        m.f(lockDir, "lockDir");
        this.f1217a = z8;
        File file = new File(lockDir, name + ".lck");
        this.f1218b = file;
        C0038a c0038a = f1215e;
        String absolutePath = file.getAbsolutePath();
        m.e(absolutePath, "lockFile.absolutePath");
        this.f1219c = c0038a.b(absolutePath);
    }

    public static /* synthetic */ void c(a aVar, boolean z8, int i9, Object obj) {
        if ((i9 & 1) != 0) {
            z8 = aVar.f1217a;
        }
        aVar.b(z8);
    }

    public final void b(boolean z8) {
        this.f1219c.lock();
        if (z8) {
            try {
                File parentFile = this.f1218b.getParentFile();
                if (parentFile != null) {
                    parentFile.mkdirs();
                }
                FileChannel channel = new FileOutputStream(this.f1218b).getChannel();
                channel.lock();
                this.f1220d = channel;
            } catch (IOException e9) {
                this.f1220d = null;
                Log.w("SupportSQLiteLock", "Unable to grab file lock.", e9);
            }
        }
    }

    public final void d() {
        try {
            FileChannel fileChannel = this.f1220d;
            if (fileChannel != null) {
                fileChannel.close();
            }
        } catch (IOException unused) {
        }
        this.f1219c.unlock();
    }
}