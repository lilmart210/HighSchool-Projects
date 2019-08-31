#lang racket
(require picturing-programs)



(define col1 "red")
(define col2 "blue")
(define board-size 8)
(define square-size 80)
;not an actual null obj

;little functions
(define switch (lambda (s)(if (string=? s col1) col2 col1)))


(define (background)
  (define bc1 "black")
  (define bc2 "tan")
  (define get-board-col (lambda(x)(if(even? x)bc2 bc1)))
  (for/fold ([img (circle 0 'solid 'red)])
            ([wid (in-range 0 board-size)])
    (above img (for/fold ([img2 (circle 0 'solid 'red)])
                         ([x (in-range wid (+ wid board-size))])
      (beside img2 (square square-size "solid"(get-board-col x)))))))
(define outline (lambda (x) (overlay (background)
                                     (square (+ 2(image-width x))
                                             'solid 'black))))
(define checker-board (outline(background)))
;-----------------end of board-----------------------------
;-----------------col1 col2 board-size square-size---------
(struct posn (x y)#:prefab)
(struct piece(psn c k)#:prefab)
;takes in a list color
(define (psn->pieces l c)
  (if (empty? l)empty (cons (piece (first l) c #f)(psn->pieces(rest l) c))))


(define (lpsn)
  (for/fold ([psn-list empty])
            ([y (in-range 1 (+ board-size 1))])
    (append (for/fold ([psn-list2 empty])
              ([x (in-range 1 (+ board-size 1))])
      (cons (posn (- (* square-size x) (/ square-size 2))
                  (- (* square-size y) (/ square-size 2)))
            psn-list2)) psn-list)))

;-------------------end of positions on board---------------
;-------------------posn piece------------------------------
(define (place-posn psnl img);this function,might not use
  (if (empty? psnl) img (place-image (text (string-append
                                      (number->string(posn-x(first psnl)))
                                      ","
                                     (number->string(posn-y(first psnl))))
                                          12 "white")
                                     (posn-x (first psnl))
                                     (posn-y (first psnl))
                                     (place-posn (rest psnl) img))))
;piece(psn color king?)
(define (place-pieces pl img)
  (define top(lambda(x)(if (piece-k x)
                           (text "K" (floor(/ square-size 2))"pink")
                           (square 0 'solid 'black))))
  (define build-piece1(lambda(x)
                        (overlay (top x)
                               (circle(/ square-size 2)'solid(piece-c x)))))
  (foldr (lambda(x y)
           (place-image (build-piece1 x)
                        (posn-x(piece-psn x))
                        (posn-y(piece-psn x))
                        y)) img pl));(LIST) IS TEMP FIX
;returns the usable spots on the board
(define (fnct l)
  (cond [(empty? l) empty]
        [(even? (length l)) (fnct(rest l))]
        [else (cons (first l)(fnct(rest l)))]))

(define (grab-on-black-edit l n fn)
  (define procA (lambda(x)
                  (append
                   x
                   (grab-on-black-edit
                    (drop l board-size)
                    (add1 n)fn))))
  
  (cond [(empty? l) empty]
        [(fn n) (procA(fnct (take l board-size)))]              
        [else (procA(fnct (reverse(take l board-size))))]))
(define (grab-on-black l n)
  (grab-on-black-edit l n odd?))
(define (grab-on-white l n)
  (grab-on-black-edit l n even?))
;don't worry about my naming convention
(define unusable-spots (grab-on-white (lpsn) 1))
(define usable-spots (grab-on-black (lpsn) 1))
(define red-king (take (reverse usable-spots) 4));(list (posn 600 40) (posn 440 40) (posn 280 40) (posn 120 40))
(define blue-king(take usable-spots 4));(list (posn 520 600) (posn 360 600) (posn 200 600) (posn 40 600))
;(place-posn usable-spots (background))
;this is a get function
;NEEDS TO BE ON BOARD
(define (posn-on-board psn l)
  (cond [(empty? l) (error "posn-on-board: point not in the List")]
                    
        [(and (<(- (posn-x (piece-psn(first l)))
                        (/ square-size 2))(posn-x psn))
                   (>(+ (posn-x (piece-psn(first l)))
                        (/ square-size 2))(posn-x psn))
                   (<(- (posn-y (piece-psn(first l)))
                        (/ square-size 2))(posn-y psn))
                   (>(+ (posn-y (piece-psn(first l)))
                        (/ square-size 2))(posn-y psn)))
              (first l)]
        [else (posn-on-board psn (rest l))]))
(define (piece=? pc1 pc2);what makes a piece a piece?|prone to edit
  (and (=(posn-x (piece-psn pc1))(posn-x(piece-psn pc2)))
               (=(posn-y (piece-psn pc1))(posn-y(piece-psn pc2)))
       (string=? (piece-c pc1)(piece-c pc2))))
(define (posn-piece=? p1 p2)
  (and (= (posn-x (piece-psn p1))(posn-x (piece-psn p2)))
       (= (posn-y (piece-psn p1))(posn-y (piece-psn p2)))))
(define (delete-piece pc l);------------------------------------------------------
  (cond [(empty? l) l]
        [(posn-piece=? pc (first l)) (rest l)]
        [else (cons (first l)(delete-piece pc (rest l)))]))
(define (delete-pieces lpc l);takes in 2 list of pieces
  (cond [(empty? lpc) l]
        [else (delete-pieces (rest lpc)(delete-piece (first lpc) l))]))
(define (highlight-board lp img);function for moves
  (define cp (make-pen "yellow" 3 "solid""round""round"))
  (for/fold ([imag img])
           ([x (in-list lp)])
   (place-image (square square-size 'outline cp)
                        (posn-x x)(posn-y x) imag)))
(define (build-piece pece);builds piece, run threw orig
  (define top(if (piece-k pece)(text "K" (floor(/ square-size 2))"pink")
                 (square 0 'solid 'black)))
  (overlay top (circle (/ square-size 2) 'solid (piece-c pece))))

(define (draw-clicked-piece pece img)
  (if(not(string? pece))
     (place-image (build-piece pece)
               (posn-x (piece-psn pece))
               (posn-y (piece-psn pece)) img)
     img))
;------------
(define (zip-up-useless pl p);returns a piece
  (if(empty? pl)empty (cons(piece(first pl)(piece-c p)(piece-k p))
                           (zip-up-useless(rest pl)p))))
;------------
(define (snap-to-grid pc);this func has a trick to it
  (on-piece? (piece-psn pc) (zip-up-useless usable-spots pc)))
;possible duplicate of posn-on-board
(define (on-piece? psn l)
  (cond [(empty? l) #f]
        [(and (<(- (posn-x (piece-psn(first l)))
                   (/ square-size 2))(posn-x psn))
              (>(+ (posn-x (piece-psn(first l)))
                   (/ square-size 2))(posn-x psn))
              (<(- (posn-y (piece-psn(first l)))
                   (/ square-size 2))(posn-y psn))
              (>(+ (posn-y (piece-psn(first l)))
                   (/ square-size 2))(posn-y psn)))
         #t]
        [else (on-piece? psn (rest l))]))
;---------------highlight functions--------------
(define (get-number s);top bottom left right
  (cond [(string=? s "t") (* -1 square-size)]
        [(string=? s "b") square-size]
        [(string=? s "l") (* -1 square-size)]
        [else square-size]))
(define (get-op-number s);top bottom left right prolly rename to get-op-string
  (cond [(string=? s "t") "b"]
        [(string=? s "b") "t"]
        [(string=? s "l") "r"]
        [else "l"]))

(define (detect-corner1 pece corn);corn is string
  (define ycord (lambda(x)(+(get-number x)(posn-y(piece-psn pece)))))
  (define xcord (lambda(x)(+(get-number x)(posn-x(piece-psn pece)))))
  (define bl (list(posn (xcord "l")(ycord "b"))
                  (posn (xcord "r")(ycord "b"))))
  (define rl(list (posn (xcord "l")(ycord "t"))
           (posn (xcord "r")(ycord "t"))))
  (cond[(piece-k pece)(append rl bl)]
       [(string=? "blue"(piece-c pece)) bl]
       [else rl]))
;piece corner-string(x,y) list-piece number of piece-in-row first-runn(firstmove) if-jump-allowed
(define (detect-corner pece csx csy lp in-row emp-row f-run turns);jump has too many flaws, very strict
  (define ycord (lambda(x y)(+(get-number x)(posn-y(piece-psn y)))))
  (define xcord (lambda(x y)(+(get-number x)(posn-x(piece-psn y)))))
  (define change-psn (lambda (s v)(struct-copy piece s[psn v])))
  (define def-change (posn (xcord csx pece)(ycord csy pece)));get-op-number
  (define def-change2(lambda(x y)(posn (xcord x pece)(ycord y pece))))
  (define op-def-cha (posn (xcord (get-op-number csx)pece) (ycord(get-op-number csy)pece)))
  
  ;(if(piece-k pece)(append d1 d2)(if(string=? "red"(piece-c pece))d1 d2))
  (cond [(or (= 2 in-row)(= 2 emp-row)(> turns 10)
             (and(on-piece? def-change lp)(string=? (piece-c pece)(piece-c(posn-on-board def-change lp)))))
         empty]
        [(and f-run (= 2(add1 emp-row))(not(on-piece? def-change lp)))
         (cons def-change empty)]
        [(and (= 2 (add1 emp-row))(not(on-piece? def-change lp)))
         empty]
        [(on-piece? def-change lp)
         (detect-corner (change-psn pece def-change) csx csy lp (add1 in-row) 0 #f(add1 turns))]
        [(not(on-piece? def-change lp))
         (cons def-change
               (cond [(piece-k pece)
                      (append (detect-corner (change-psn pece def-change) (get-op-number csx)
                                      csy lp 0 (add1 emp-row)#f(add1 turns))
                       (detect-corner (change-psn pece def-change) csx (get-op-number csy)
                                      lp 0 (add1 emp-row)#f (add1 turns))
                       (detect-corner (change-psn pece def-change) csx csy lp 0 (add1 emp-row)#f(add1 turns))
                       )]
                     [(string=? "red"(piece-c pece))
                      (append (detect-corner (change-psn pece def-change) (get-op-number csx)
                                             csy lp 0 (add1 emp-row)#f(add1 turns))
                              (detect-corner (change-psn pece def-change) csx csy lp
                                             0 (add1 emp-row)#f(add1 turns)))];watch for circle of death
                     [else (append (detect-corner (change-psn pece def-change)(get-op-number csx)csy
                                      lp 0 (add1 emp-row)#f (add1 turns))
                              (detect-corner (change-psn pece def-change) csx csy lp
                                             0 (add1 emp-row)#f(add1 turns)))]))]
        [else empty]));tried to cover every case here, no reason for this empty to run



(define (detect-spots-move pece lpiece);this works here
  (cond [(piece-k pece)
         (append (detect-corner pece "r""t" lpiece 0 1 #t 0)
                 (detect-corner pece "l""b" lpiece 0 1 #t 0)
                 (detect-corner pece "r""b" lpiece 0 1 #t 0)
                 (detect-corner pece "l""t" lpiece 0 1 #t 0))]
        [(string=? "red"(piece-c pece))
         (append (detect-corner pece "r""t" lpiece 0 1 #t 0)
                 (detect-corner pece "l""t" lpiece 0 1 #t 0))]
        [else (append(detect-corner pece "l""b" lpiece 0 1 #t 0)
                     (detect-corner pece "r""b" lpiece 0 1 #t 0))]))

   


                  
                  
        
        

              
;------------end of highlight functions----------
;-------------start of drag-functions(move-detection-deletion)
(define p1 (posn 3 4))
(define p2 (posn 4 8))
(define (count-occur l e)
  (cond [(empty? l) 0]
        [(and (=(posn-x(first l))(posn-x e))
              (=(posn-y(first l))(posn-y e)))
         (+ 1 (count-occur (rest l)e))]
        [else (count-occur (rest l) e)]))
(define (single-occur l);this function and all its parts are tested
  (define remlist (lambda()(remove*(list(first l))(rest l))))
  (cond [(empty? l) empty]
        [(< 1 (count-occur l (first l)))
         (cons (first l)(single-occur (remlist)))]
        [else (cons (first l)(single-occur (rest l)))]))

(define (grab-on-psn psn lps);not tested
  (cond [(empty? lps) empty];retList
        [(on-piece? psn lps);(zip-up-useless lps (first lps))
         (list (piece-psn(posn-on-board psn lps)))]
        [else (grab-on-psn psn (rest lps))]))

(define (grab-on-psns psnl lps)
  (cond [(empty? psnl) empty]
        [else (cons (grab-on-psn(first psnl) lps)(grab-on-psns(rest psnl) lps))]))

(define (detain-to-path l)
  l)
(define (middle-posn psn1 psn2)
  (posn (/(+(posn-x psn1)(posn-x psn2))2)(/(+(posn-y psn1)(posn-y psn2))2)))

(define (grab-middle l);takes in list of posns, can be adjused
  (cond [(empty? l) empty]
        [(= 1 (length l)) empty]
        [else (cons (middle-posn(first l)(second l))(grab-middle(rest l)))]))

(define (detect-blue-kings lp lpsn)
  (cond [(empty? lpsn) lp]
        [(and (on-piece? (first lpsn) lp)(string=? "blue"(piece-c(posn-on-board(first lpsn)lp))))
         (detect-blue-kings(cons (struct-copy piece (posn-on-board(first lpsn) lp)[k #t])
                                 (delete-piece (posn-on-board (first lpsn) lp) lp))(rest lpsn))]
        [else (detect-blue-kings lp (rest lpsn))]))
(define (detect-red-kings lp lpsn)
  (cond [(empty? lpsn) lp]
        [(and (on-piece? (first lpsn) lp)(string=? "red"(piece-c(posn-on-board(first lpsn)lp))))
         (detect-red-kings(cons (struct-copy piece (posn-on-board(first lpsn) lp)[k #t])
                                 (delete-piece (posn-on-board (first lpsn) lp) lp))(rest lpsn))]
        [else (detect-red-kings lp (rest lpsn))]))

(define (detect-kings l);list of pieces
  (detect-red-kings (detect-blue-kings l blue-king)red-king))


;-----------------------------piece functions above----------------------

  
(define (spawn-stuff m)
  m)
(define (move-players m x y e);pc3 is piece coords
  (define pc3 (lambda() (posn-on-board (posn x y)(keep-lps m))))
  (define hlpsnts (lambda()(zip-up-useless (keep-lp m)
                                    (piece(posn 0 0)
                                          (piece-c(keep-cp m))
                                          (piece-k(keep-cp m))))))
  (define zip-use (lambda() (zip-up-useless;takes in piece list of posns
                             (keep-lp m)
                             (piece(posn 0 0)(piece-c(keep-cp m))
                                   (piece-k(keep-cp m))))))
      (cond[(and(string=? e "button-down")(on-piece?(posn x y)(keep-lps m))
                (string=? (keep-pt m)(piece-c(posn-on-board(posn x y)(keep-lps m)))))
         (make-package m
                       (struct-copy keep m
                                    [lps (delete-piece (pc3) (keep-lps m))]
                                    [cp (pc3)]
                                    [ogp (pc3)]
                                    [htp (cons (piece-psn(pc3))(keep-htp m))]
                                    [lp (detect-spots-move (pc3)(keep-lps m))]))]
           [(and(string=? e "drag")(not(string?(keep-cp m))))
            (make-package m
              (struct-copy keep m
                          [cp (struct-copy piece (keep-cp m)[psn (posn x y)])]
                           ;htp is a very big list|unable to detain b/c nature of the code
                          [htp (single-occur(append (grab-on-psn
                           (posn x y)
                          (zip-up-useless(keep-lp m)(keep-cp m)))(keep-htp m)))]))]
           [(and (not(string?(keep-cp m)))(string=? "button-up" e)
             (not(on-piece? (posn x y)(zip-use))))
         (make-package m (struct-copy keep m;this part work
                      [lps (cons(keep-ogp m)(keep-lps m))]
                      [htp empty]
                      [lp empty];clears highlighted spots
                      [cp "null"]))]
        [(and(not(string?(keep-cp m)));(cons(snap-to-grid (keep-cp m))(keep-lps m))
             (string=? e "button-up")(on-piece? (posn x y)(zip-use)));(println (grab-middle(keep-htp m)))
           (make-package m (struct-copy keep m 
                      [lps (detect-kings (delete-pieces;zip-up-uselessworks
                            (zip-up-useless(grab-middle(keep-htp m))
                                           (posn-on-board(piece-psn(keep-cp m))(zip-use)))
                            (cons(posn-on-board(piece-psn(keep-cp m))(zip-use))
                                 (keep-lps m))))]
                      [ogp (posn-on-board(posn x y)(zip-use))]
                      [pt (switch (keep-pt m))]
                      [lp empty]
                      [htp empty]
                      [cp "null"]))];this is never called
         
        [else (make-package m m)]))
      
      
;DRAW HANDLER IS ALMOST DONE
(define (draw-dim-pieces lpsn pece img)
  (define cir(lambda()(circle (/ square-size 2) 100 (piece-c pece))))
  (if(string? pece)img(for/fold ([im img])
            ([x (in-list lpsn)])
    (place-image (if (piece-k pece) (overlay (text "K" (floor(/ square-size 2))"pink")(cir))(cir))
                 (posn-x x)(posn-y x) im))))
(define (draw-stuff m)
  
             (draw-dim-pieces (single-occur(keep-htp m)) (keep-cp m)
                   (draw-clicked-piece (keep-cp m);place-piecesproblem
                   (highlight-board (keep-lp m)(place-pieces (keep-lps m)(background))))))
;lps is being replaced with a single obj

;playerTurn PiecesIn(list) ClickedPiece(obj) HighlightedPlaces(listpsns)
;original-clicked-piece highlighted-tracked-pieces
(struct keep (pt lps cp lp ogp htp) #:prefab)
(define rp(psn->pieces(take usable-spots 12)"red"))
(define bp(psn->pieces(drop usable-spots (-(length usable-spots)12))"blue"))
;(piece (posn 300 20) "blue" #t)
(define start-it (keep "blue"(append rp bp) "null"
  (list)(piece(posn 0 0)"green" #f) empty))

(define (debug m k);delete this later
  (cond [(key=? "d" k) ((lambda()(println (keep-cp m))m))]
        [(key=? "r" k) start-it]
        [(key=? "t" k)(struct-copy keep m[pt (switch (keep-pt m))])]
        [else m]))


;will have to switch this out with the on-key
(define (onrcv m msg)
  msg)


(define (checker-world nam)
  (big-bang start-it
    (on-tick spawn-stuff)
    (on-mouse move-players)
    (on-key debug)
    (on-receive onrcv)
    (name nam)
    (register LOCALHOST)
    (state #f)
    (close-on-stop #t)
    (on-draw draw-stuff)))
;this game is trully done
;finished the checkers game
(define launch (launch-many-worlds (checker-world "1")(checker-world "2")))
(provide start-it checker-world)

                   

      
    






































    

