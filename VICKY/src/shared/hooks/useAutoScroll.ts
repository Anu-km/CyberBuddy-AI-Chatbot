import { useEffect, useRef } from "react";

export function useAutoScroll(dep: any) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    ref.current?.scrollTo({ top: ref.current.scrollHeight, behavior: "smooth" });
  }, [dep]);

  return ref;
}
