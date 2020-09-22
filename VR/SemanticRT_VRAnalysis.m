BCovert=csv2struct('RTData_48.csv');
BOvert=csv2struct('RTData_47.csv');
BBBOvert=csv2struct('RTData_57.csv');

angles=unique(BCovert.Angle)

for i = 1:length(angles)
   ind=find(BCovert.Angle==angles(i));
   meanRTCovert(i)=mean(BCovert.ReactionTime(ind));
    
end


plot(1000*meanRTCovert,angles,'-o')
xlim([100 600])

xlabel('time(ms)')
ylabel('Angle (deg)')

for i = 1:length(angles)
   ind=find(BOvert.Angle==angles(i));
   meanRTOvert(i)=mean(BOvert.ReactionTime(ind));
    
end

hold on
plot(1000*meanRTOvert,angles,'-o')



for i = 1:length(angles)
   ind=find(BBBOvert.Angle==angles(i));
   meanRTBBBOvert(i)=mean(BBBOvert.ReactionTime(ind));
    
end

hold on
plot(1000*meanRTBBBOvert,angles,'-o')


legend('B Covert', 'B Overt', 'BBB Overt')


