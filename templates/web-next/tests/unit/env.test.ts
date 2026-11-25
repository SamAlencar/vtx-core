import { describe, expect, it } from "vitest";
import { lerEnv } from "../../lib/env";

describe("lerEnv", () => {
  it("aceita env vazio no template (build sem segredo)", () => {
    expect(lerEnv({})).toEqual({
      NEXT_PUBLIC_SUPABASE_URL: "",
      NEXT_PUBLIC_SUPABASE_ANON_KEY: "",
    });
  });

  it("aceita uma URL válida do Supabase", () => {
    const env = lerEnv({
      NEXT_PUBLIC_SUPABASE_URL: "https://exemplo.supabase.co",
      NEXT_PUBLIC_SUPABASE_ANON_KEY: "anon-public",
    });
    expect(env.NEXT_PUBLIC_SUPABASE_URL).toBe("https://exemplo.supabase.co");
  });

  it("rejeita URL malformada", () => {
    expect(() =>
      lerEnv({ NEXT_PUBLIC_SUPABASE_URL: "nao-e-url" }),
    ).toThrow();
  });
});
