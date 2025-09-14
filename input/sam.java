class Main {
    public static void main(String[] args) {
        if (false) {
            System.out.println("Never executes");
        }
        int y = 2 + 2;
        if (3*3 == 9) {
            System.out.println("Opaque");
        }
        return;
        System.out.println("Dead code");
    }
}
