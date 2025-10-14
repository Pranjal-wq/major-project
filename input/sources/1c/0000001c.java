package A5;

/* loaded from: classes2.dex */
public enum b {
    TRACE_EVENT_RATE_LIMITED("_fstec"),
    NETWORK_TRACE_EVENT_RATE_LIMITED("_fsntc"),
    TRACE_STARTED_NOT_STOPPED("_tsns"),
    FRAMES_TOTAL("_fr_tot"),
    FRAMES_SLOW("_fr_slo"),
    FRAMES_FROZEN("_fr_fzn");
    

    /* renamed from: a  reason: collision with root package name */
    private String f202a;

    b(String str) {
        this.f202a = str;
    }

    @Override // java.lang.Enum
    public String toString() {
        return this.f202a;
    }
}