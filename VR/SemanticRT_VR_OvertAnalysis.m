close all
A=csv2struct('RTData_57.csv');
B=csv2struct('fove_recorded_results_57.csv');
angles=unique(A.Angle);

for i = 1:length(angles)
   ind=find(A.Angle==angles(i));
   meanRT(i)=mean(A.ReactionTime(ind));
    
end

scatter(angles,meanRT)

eyeAngleLeft=atan2d(B.leftGaze_direction_z,B.leftGaze_direction_x)-median(atan2d(B.leftGaze_direction_z,B.leftGaze_direction_x));
eyeAngleRight=atan2d(B.rightGaze_direction_z,B.rightGaze_direction_x)-median(atan2d(B.rightGaze_direction_z,B.rightGaze_direction_x));




for j=1:A.TrialNumber(end)
    indTrialTime=find(B.frameTime>A.StimTime(j)&B.frameTime<A.ButtonTime(j)+0.2);
    timeTrial=B.frameTime(indTrialTime)-B.frameTime(indTrialTime(1));
    plot(timeTrial,eyeAngleLeft(indTrialTime)-eyeAngleLeft(indTrialTime(1)));
    hold on
    gradEye=gradient(eyeAngleLeft(indTrialTime)-eyeAngleLeft(indTrialTime(1)));
%     saccadeTime= timeTrial(find(gradEye>max(gradEye)/100));
%     saccadeTimeStart(j)=min(saccadeTime);
%     saccadeTimeEnd(j)=max(saccadeTime);
   
    
    
    
end

title ('FOVE VR Eye tracking Overt BBB')
ylabel('Stimulation Angle (deg)')
xlabel('time (s)')



ind40=find(A.Angle==-30);
for j=1:length(ind40)
    indTrialTime=find(B.frameTime>A.StimTime(ind40(j))&B.frameTime<A.ButtonTime(ind40(j))+0.2);
    plot(B.frameTime(indTrialTime)-B.frameTime(indTrialTime(1)),eyeAngleRight(indTrialTime)-eyeAngleRight(indTrialTime(1)));
    hold on
    
end



ind40=find(A.Angle==10);
for j=1:length(ind40)
    indTrialTime=find(B.frameTime>A.StimTime(ind40(j))&B.frameTime<A.ButtonTime(ind40(j))+0.1);
    timeTrial=B.frameTime(indTrialTime)-B.frameTime(indTrialTime(1));
    gradEye=gradient(eyeAngleRight(indTrialTime)-eyeAngleRight(indTrialTime(1)));
    saccadeTime= timeTrial(find(gradm30>max(gradm30)/100));
    saccadeTimeStart(j)=min(saccadeTime);
    saccadeTimeEnd(j)=max(saccadeTime);
    plot(B.frameTime(indTrialTime)-B.frameTime(indTrialTime(1)),gradient(eyeAngleRight(indTrialTime)-eyeAngleRight(indTrialTime(1))));
    hold on
    
end

timem30=B.frameTime(indTrialTime)-B.frameTime(indTrialTime(1));
gradm30=gradient(eyeAngleRight(indTrialTime)-eyeAngleRight(indTrialTime(1)));
saccadeTime=timem30(find((gradm30)>max((gradm30))/100));
saccadeTimeStart=min(saccadeTime);
saccadeTimeEnd=max(saccadeTime);





