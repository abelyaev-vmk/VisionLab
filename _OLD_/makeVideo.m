function makeVideo(in_dir, out_file)
    
    images = dir([in_dir '*.jpg']); %array of images' filenames
    n_images = length(images); % total number of images
    fps = 20;
    videoWriter = vision.VideoFileWriter(out_file,'FrameRate', fps, 'VideoCompressor', 'DV Video Encoder');
    i = 1;
    display(i);
    while i < n_images
        frame = im2double(imread([in_dir images(i).name]));
        videoWriter.step(frame);
        display(i);
        i = i + 1;
    end