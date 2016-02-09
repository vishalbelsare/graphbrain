(ns graphbrain.web.handlers.docs
  (:require [graphbrain.db.gbdb :as gb]
            [graphbrain.web.common :as common]
            [graphbrain.web.cssandjs :as css+js]
            [graphbrain.web.views.docs :as docs]
            [graphbrain.web.encoder :as enc]
            [markdown.core :as md]))

(defn- data
  [user ctxt ctxts]
  #_{:ctxts (contexts/contexts-map ctxts (:id user))
   :context (contexts/context-data (:id user) (:id user))})

(defn- js
  [user ctxt ctxts]
  (str "var ptype='help';"
       "var data='" (enc/encode (pr-str
                      (data user ctxt ctxts))) "';"))

(defn handle
  [request]
  #_(let
      [user (common/get-user request)
       page (:* (:route-params request))
       ctxts (contexts/active-ctxts (:id user) user)
       ctxt (contexts/context-data (:id user) (:id user))
       html (md/md-to-html-string
             (slurp
              (clojure.java.io/resource
               (str "docs/" page ".md"))))]
    (common/log request "docs")
    (docs/docs :title "Docs"
               :css-and-js (css+js/css+js)
               :user user
               :ctxt ctxt
               :js (js user ctxt ctxts)
               :html html)))
