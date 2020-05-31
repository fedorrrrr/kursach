; ModuleID = '<string>'

target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@max = internal unnamed_addr global i32 undef
@max2 = internal unnamed_addr global i32 undef
@fstr0 = internal constant [5 x i8] c"%i \0A\00"
@fstr1 = internal constant [5 x i8] c"%i \0A\00"
@fstr2 = internal constant [5 x i8] c"%i \0A\00"
@fstr3 = internal constant [5 x i8] c"%i \0A\00"
@fstr4 = internal constant [5 x i8] c"%i \0A\00"
@fstr5 = internal constant [5 x i8] c"%i \0A\00"
@fstr6 = internal constant [5 x i8] c"%i \0A\00"
@fstr7 = internal constant [5 x i8] c"%i \0A\00"
@fstr8 = internal constant [5 x i8] c"%i \0A\00"
@fstr11 = internal constant [5 x i8] c"%i \0A\00"

; Function Attrs: nounwind
define void @main()  {
entry:
  %.9 = tail call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @fstr1, i64 0, i64 0), i32 1)
  %.20 = tail call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @fstr2, i64 0, i64 0), i32 5)
  %.27 = tail call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @fstr3, i64 0, i64 0), i32 2)
  %.38 = tail call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @fstr4, i64 0, i64 0), i32 10)
  %.45 = tail call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @fstr5, i64 0, i64 0), i32 3)
  %.56 = tail call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @fstr6, i64 0, i64 0), i32 15)
  %.63 = tail call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @fstr7, i64 0, i64 0), i32 4)
  %.74 = tail call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @fstr8, i64 0, i64 0), i32 20)
  %.106 = tail call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @fstr11, i64 0, i64 0), i32 36)
  ret void
}

; Function Attrs: nounwind
declare i32 @printf(i8* nocapture readonly, ...) 

; Function Attrs: nounwind
define i32 @function(i32 %.1, i32 %.2)  {
entry:
  %.8 = icmp slt i32 %.1, %.2
  br i1 %.8, label %entry.if, label %entry.else

entry.if:                                         ; preds = %entry
  store i32 %.2, i32* @max, align 4
  %.20.pre = load i32, i32* @max2, align 4
  br label %entry.endif

entry.else:                                       ; preds = %entry
  store i32 %.1, i32* @max2, align 4
  br label %entry.endif

entry.endif:                                      ; preds = %entry.else, %entry.if
  %.20 = phi i32 [ %.1, %entry.else ], [ %.20.pre, %entry.if ]
  %.22 = tail call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @fstr0, i64 0, i64 0), i32 %.20)
  %.23 = load i32, i32* @max, align 4
  ret i32 %.23
}

; Function Attrs: nounwind
declare void @llvm.stackprotector(i8*, i8**) #0

attributes #0 = { nounwind }
