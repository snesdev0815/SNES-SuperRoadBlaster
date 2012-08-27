  (define (batch-convert-indexed pattern colors)
  (let* ((filelist (cadr (file-glob pattern 1))))
    (while (not (null? filelist))
           (let* ((filename (car filelist))
                  (image (car (gimp-file-load RUN-NONINTERACTIVE
                                              filename filename)))
                  (drawable (car (gimp-image-get-active-layer image))))
                
                (plug-in-sel-gauss RUN-NONINTERACTIVE image drawable 10.0 25)
                (gimp-image-convert-indexed image 0 0 colors 0 0 "")
             
             (gimp-file-save RUN-NONINTERACTIVE
                             image drawable filename filename)
             (gimp-image-delete image))
           (set! filelist (cdr filelist)))))
