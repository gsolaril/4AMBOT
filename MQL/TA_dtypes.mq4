#include <Clustering.mqh>

LineArray::LineArray(double minStep, uchar maxLength = 32, string filter = "kMeans") {
    this.mStep = minStep ; this.mLength = maxLength ; this.mode = cMode; }

LineArray::clusterModes { kMeans = 0; mixGDE = 1; mShift = 2; hClust = 3; }

LineArray::values(double & values[]) {
    uchar n = ArraySize(this.Values);
    n = ArrayResize(values, n);
    n = ArrayCopy(values, this.Values); }

LineArray::dtimes(datetime & values[]) {
    uchar n = ArraySize(this.dTimes);
    n = ArrayResize(values, n);
    n = ArrayCopy(values, this.dTimes); }

LineArray::length() { return this.Length; }

LineArray::min_step() { return this.mStep; }

LineArray::max_length() { return this.mLength; }

LineArray::cmode() { return this.cMode; }

LineArray::append(datetime dtime, double value, bool draw = true) {
    value = MathRound(value/this.minStep)*this.minStep;
    double above, below, Copy_v[] = {}, Copy_d[] = {};
    ArrayCopy(Copy_v, this.Values);
    ArrayCopy(Copy_d, this.dTimes);
    for (int i = 0; i < this.lines; i++) {
        above = this.Values[i] + this.mStep;
        below = this.Values[i] - this.mStep;
        if (below < value) { if (value < above) return; }
        else break; }
    ArrayResize(this.Values, this.lines + 1);
    ArrayResize(this.dTimes, this.lines + 1);
    ArrayCopy(this.Values, Copy_v, i + 1, i);
    ArrayCopy(this.Values, Copy_d, i + 1, i);
    if (draw) this.draw(value, this.color);
    this.Values[i] = value;
    this.dTimes[i] = dtime;
    if (++this.lines > this.mLength) this.erase(); }

LineArray::bind(double & bounds, double value) {
    bounds = {0, DBL_MAX};
    if (this.lines == 0) return;
    ArrayResize(bounds, 2);
    uchar e = this.lines - 1;
    for (int i = 0; i < this.lines; i++) {
        if (this.Values[i] > value) break; }
    if (i > 0) bounds[0] = this.Values[i - 1];
    if (i < e) bounds[1] = this.Values[i - 0]; }

LineArray::cluster(double & values[]) {

}

LineArray::draw(color marker, double p) {
    try {
        string tag = " " + this.tag;
        tag = TimeToString(this.dTime[i]) + tag;
        ObjectCreate(0, tag, OBJ_TREND, 0, dt, p, dt, p);
        ObjectSetInteger(0, tag, OBJPROP_RAY_RIGHT, true);
        ObjectSetInteger(0, tag, OBJPROP_HIDDEN, false);
        ObjectSetInteger(0, tag, OBJPROP_COLOR, marker); }
    catch(e) {} }

LineArray::erase() {
    uchar i = --this.lines;
    datetime t, t_min = TimeCurrent();
    

    for (int i = 0, i < e, i++) {
        if (i == this.first) continue;
        t = this.dTimes[i];
        if (t < t_min) this.first = i;
        if (i < this.first) continue;
        this.Values[i] = this.Values[i + 1];
        this.dTimes[i] = this.Values[i + 1]; }
    ArrayResize(this.Values, this.lines);
    ArrayResize(this.dTimes, this.lines);

    
}