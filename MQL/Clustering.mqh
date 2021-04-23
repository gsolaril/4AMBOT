class Clustering1D {

    public:
        static const void kMeans(double & values, uchar K, double mDist);
        static const void mixGDE(double & values, double bw);
        static const void mShift(double & values, double bw);
        static const void hClust(double & values, double mDist);
}