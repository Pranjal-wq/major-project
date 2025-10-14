package C3;

import android.graphics.Canvas;

/* loaded from: classes2.dex */
public class a {

    /* renamed from: C3.a$a  reason: collision with other inner class name */
    /* loaded from: classes2.dex */
    public interface AbstractC0039a {
        void a(Canvas canvas);
    }

    public static int a(Canvas canvas, float f9, float f10, float f11, float f12, int i9) {
        return canvas.saveLayerAlpha(f9, f10, f11, f12, i9);
    }
}