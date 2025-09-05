; !(bind! &medical_kb (new-space))
; !(import! &rules rules)

; !(add-reduct &medical_kb (superpose ((get-atoms &rules))))
; !(import! &facts kb)
; !(add-reduct &medical_kb (superpose ((get-atoms &facts))))

;; Utility function to convert numbers to MeTTa natural numbers
(= (fromNumber $n) (if (<= $n 0) Z (S (fromNumber (- $n 1)))))

(: bc (-> $a                           ; Knowledge base space
          Nat                          ; Maximum depth
          $b                           ; Query
          $b))                         ; Result

;; Base case
(= (bc $kb $_ (: $prf $ccln)) (match $kb (: $prf $ccln) (: $prf $ccln)))

;; Recursive step
(= (bc $kb (S $k) (: ($prfabs $prfarg) $ccln))
   (let* (((: $prfabs (-> $prms $ccln)) (bc $kb $k (: $prfabs (-> $prms $ccln))))
          ((: $prfarg $prms) (bc $kb $k (: $prfarg $prms))))
     (: ($prfabs $prfarg) $ccln)))

;; Forward DTL Curried
(: fcc (-> $a                            ; Knowledge base space
           Nat                           ; Maximum depth
           $b                            ; Source
           $b))                          ; Conclusion

;; Base case
(= (fcc $kb $_ (: $prf $prms)) (: $prf $prms))

;; Recursive step
(= (fcc $kb (S $k) (: $prfarg $prms))
   (let (: $prfabs (-> $prms $ccln)) (bc $kb $k (: $prfabs (-> $prms $ccln)))
     (fcc $kb $k (: ($prfabs $prfarg) $ccln))))
(= (fcc $kb (S $k) (: $prfabs (-> $prms $ccln)))
    (let (: $prfarg $prms) (bc $kb $k (: $prfarg $prms))
     (fcc $kb $k (: ($prfabs $prfarg) $ccln))))